import json
import os
from pathlib import Path

from confluent_kafka import Consumer, KafkaException

from health_engine import evaluate_vehicle
from history import (
    initialize_database,
    save_vehicle_reading,
    load_active_states
)


# ==================================================
# 1. CONFIGURATION
# ==================================================

TOPIC = "athena_telemetry"
PROJECT_ROOT = Path(__file__).resolve().parent.parent
ENV_FILE = PROJECT_ROOT / ".env"

vehicle_states = {}


# ==================================================
# 2. LOAD ENVIRONMENT VARIABLES
# ==================================================

def load_environment():

    if not ENV_FILE.exists():
        raise FileNotFoundError(
            f"Environment file not found: {ENV_FILE}"
        )

    for raw_line in ENV_FILE.read_text().splitlines():

        line = raw_line.strip()

        if not line or line.startswith("#"):
            continue

        if line.startswith("export "):
            line = line[7:].strip()

        if "=" not in line:
            continue

        key, value = line.split("=", 1)

        key = key.strip()
        value = value.strip()

        if not key:
            continue

        if (
            len(value) >= 2
            and value[0] == value[-1]
            and value[0] in ("'", '"')
        ):
            value = value[1:-1]

        os.environ.setdefault(key, value)


# ==================================================
# 3. KAFKA CONFIGURATION
# ==================================================

def build_kafka_config():

    load_environment()

    required_variables = [
        "KAFKA_BOOTSTRAP_SERVERS",
        "KAFKA_USERNAME",
        "KAFKA_PASSWORD"
    ]

    missing = [
        variable
        for variable in required_variables
        if not os.getenv(variable)
    ]

    if missing:
        raise RuntimeError(
            "Missing Kafka environment variables: "
            + ", ".join(missing)
            + ". Check your local .env file."
        )

    return {
        "bootstrap.servers": os.environ[
            "KAFKA_BOOTSTRAP_SERVERS"
        ],
        "security.protocol": "SASL_PLAINTEXT",
        "sasl.mechanisms": "SCRAM-SHA-512",
        "sasl.username": os.environ["KAFKA_USERNAME"],
        "sasl.password": os.environ["KAFKA_PASSWORD"],
        "group.id": "athena_backend_consumer",
        "auto.offset.reset": "latest",
        "enable.auto.commit": False,
        "enable.auto.offset.store": False
    }


# ==================================================
# 4. PROCESS TELEMETRY
# ==================================================

def analyse_record(data):

    vehicle_id = data.get("asset_id", "UNKNOWN")
    previous_state = vehicle_states.get(vehicle_id)

    result, current_state = evaluate_vehicle(
        data,
        previous_state
    )

    try:
        saved = save_vehicle_reading(data, result)

    except Exception as error:
        print(f"DATABASE SAVE FAILED: {error}")
        print("Vehicle state NOT advanced.")
        return False

    if not saved:
        print(
            "REPLAY IGNORED: Already persisted telemetry "
            f"for {vehicle_id}."
        )
        return True

    vehicle_states[vehicle_id] = current_state

    print("\n" + "=" * 60)
    print(f"VEHICLE ID     : {result['asset_id']}")
    print(f"HEALTH SCORE   : {result['health_score']}")
    print(f"HEALTH STATUS  : {result['status']}")
    print(f"ACTIVE ISSUES  : {len(result['active_issues'])}")

    for issue in result.get("data_quality_issues", []):
        print(f"[DATA QUALITY] {issue}")

    for issue in result["new_alerts"].values():
        print(
            f"[NEW {issue['severity']}] "
            f"{issue['message']}"
        )

    for issue in result["ongoing_alerts"].values():
        print(
            f"[ONGOING {issue['severity']}] "
            f"{issue['message']}"
        )

    for issue in result["resolved_alerts"].values():
        print(f"[RESOLVED] {issue['message']}")

    if result["status"] == "HEALTHY":
        print("No active anomalies detected.")

    print("=" * 60)

    return True


# ==================================================
# 5. KAFKA CONSUMER
# ==================================================

def main():

    global vehicle_states

    config = build_kafka_config()

    initialize_database()
    vehicle_states = load_active_states()

    consumer = Consumer(config)
    consumer.subscribe([TOPIC])

    print("\nATHENA VEHICLE HEALTH ENGINE STARTED")
    print(f"Listening to Kafka topic: {TOPIC}")
    print(f"Restored vehicle states: {len(vehicle_states)}")
    print("Waiting for vehicle telemetry...\n")

    try:

        while True:

            message = consumer.poll(1.0)

            if message is None:
                continue

            if message.error():
                print(f"Kafka error: {message.error()}")
                continue

            try:
                raw_data = message.value().decode("utf-8")
                vehicle_data = json.loads(raw_data)

                if not isinstance(vehicle_data, dict):
                    print(
                        "Skipping invalid telemetry: "
                        "expected JSON object."
                    )
                    consumer.commit(
                        message=message,
                        asynchronous=False
                    )
                    continue

            except (UnicodeDecodeError, json.JSONDecodeError) as error:
                print(f"Message decoding error: {error}")
                consumer.commit(
                    message=message,
                    asynchronous=False
                )
                continue

            try:
                success = analyse_record(vehicle_data)

                if not success:
                    continue

                consumer.commit(
                    message=message,
                    asynchronous=False
                )

            except KafkaException as error:
                print(f"Kafka processing/commit error: {error}")

            except Exception as error:
                print(f"Vehicle processing error: {error}")

    except KeyboardInterrupt:
        print("\nStopping Athena consumer...")

    except KafkaException as error:
        print(f"Kafka connection error: {error}")

    finally:
        consumer.close()
        print("Kafka consumer closed.")


# ==================================================
# 6. ENTRY POINT
# ==================================================

if __name__ == "__main__":
    main()
