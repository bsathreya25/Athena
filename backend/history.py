
import json
import sqlite3
import hashlib

from pathlib import Path
from datetime import datetime, timezone
from contextlib import contextmanager


# ==================================================
# 1. DATABASE CONFIGURATION
# ==================================================

PROJECT_ROOT = Path(__file__).resolve().parent.parent
DATA_DIR = PROJECT_ROOT / "data"
DB_PATH = DATA_DIR / "athena.db"


# ==================================================
# 2. DATABASE CONNECTION
# ==================================================

@contextmanager
def get_connection():

    DATA_DIR.mkdir(parents=True, exist_ok=True)

    connection = sqlite3.connect(DB_PATH)

    try:
        yield connection
        connection.commit()

    except Exception:
        connection.rollback()
        raise

    finally:
        connection.close()


# ==================================================
# 3. TELEMETRY IDENTITY
# ==================================================

def generate_reading_id(data):

    canonical_data = json.dumps(
        data,
        sort_keys=True,
        separators=(",", ":"),
        ensure_ascii=False
    )

    return hashlib.sha256(
        canonical_data.encode("utf-8")
    ).hexdigest()


# ==================================================
# 4. DATABASE INITIALIZATION + MIGRATION
# ==================================================

def initialize_database():

    with get_connection() as connection:

        cursor = connection.cursor()

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS vehicle_readings (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                asset_id TEXT NOT NULL,
                timestamp TEXT NOT NULL,
                health_score INTEGER,
                status TEXT,
                active_issues_json TEXT,
                telemetry_json TEXT
            )
        """)

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS alert_history (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                asset_id TEXT NOT NULL,
                timestamp TEXT NOT NULL,
                issue_id TEXT NOT NULL,
                event_type TEXT NOT NULL,
                severity TEXT,
                message TEXT
            )
        """)

        # Inspect existing schema.
        cursor.execute("PRAGMA table_info(vehicle_readings)")

        columns = {
            row[1] for row in cursor.fetchall()
        }

        # Add idempotency column to older databases.
        if "idempotency_key" not in columns:

            cursor.execute("""
                ALTER TABLE vehicle_readings
                ADD COLUMN idempotency_key TEXT
            """)

        # Backfill existing telemetry identities.
        cursor.execute("""
            SELECT id, telemetry_json
            FROM vehicle_readings
            WHERE idempotency_key IS NULL
        """)

        old_rows = cursor.fetchall()

        for row_id, telemetry_json in old_rows:

            try:

                data = json.loads(telemetry_json)

                if not isinstance(data, dict):
                    continue

                reading_id = generate_reading_id(data)

                # Avoid assigning the same identity to multiple
                # historical rows if duplicates already exist.
                cursor.execute("""
                    SELECT 1
                    FROM vehicle_readings
                    WHERE idempotency_key = ?
                    LIMIT 1
                """, (reading_id,))

                if cursor.fetchone() is not None:
                    continue

                cursor.execute("""
                    UPDATE vehicle_readings
                    SET idempotency_key = ?
                    WHERE id = ?
                """, (reading_id, row_id))

            except (json.JSONDecodeError, TypeError, ValueError):

                print(
                    f"Migration skipped malformed telemetry "
                    f"for reading ID {row_id}"
                )

        # Enforce uniqueness after backfilling.
        cursor.execute("""
            CREATE UNIQUE INDEX IF NOT EXISTS
            idx_vehicle_reading_identity
            ON vehicle_readings (idempotency_key)
        """)

        cursor.execute("""
            CREATE INDEX IF NOT EXISTS idx_vehicle_asset
            ON vehicle_readings (asset_id, timestamp)
        """)

        cursor.execute("""
            CREATE INDEX IF NOT EXISTS idx_alert_asset
            ON alert_history (asset_id, timestamp)
        """)

    print(f"SQLite database ready: {DB_PATH}")


# ==================================================
# 5. RESTORE PREVIOUS VEHICLE STATES
# ==================================================

def load_active_states():

    vehicle_states = {}

    with get_connection() as connection:

        cursor = connection.cursor()

        cursor.execute("""
            SELECT asset_id, active_issues_json
            FROM vehicle_readings
            WHERE id IN (
                SELECT MAX(id)
                FROM vehicle_readings
                GROUP BY asset_id
            )
        """)

        rows = cursor.fetchall()

        for asset_id, issues_json in rows:

            try:

                issues = json.loads(
                    issues_json
                ) if issues_json else {}

                vehicle_states[asset_id] = {
                    "issues": issues
                }

            except (json.JSONDecodeError, TypeError):

                print(
                    f"Could not restore state for {asset_id}"
                )

    print(
        f"Restored previous states for "
        f"{len(vehicle_states)} vehicles."
    )

    return vehicle_states


# ==================================================
# 6. SAVE VEHICLE TELEMETRY AND HEALTH
# ==================================================

def save_vehicle_reading(data, result):

    asset_id = result["asset_id"]

    timestamp = data.get("timestamp")

    if not timestamp:

        timestamp = datetime.now(
            timezone.utc
        ).isoformat()

    reading_id = generate_reading_id(data)

    with get_connection() as connection:

        cursor = connection.cursor()

        cursor.execute("""
            INSERT OR IGNORE INTO vehicle_readings (
                asset_id,
                timestamp,
                health_score,
                status,
                active_issues_json,
                telemetry_json,
                idempotency_key
            )
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (
            asset_id,
            timestamp,
            result["health_score"],
            result["status"],
            json.dumps(result["active_issues"]),
            json.dumps(data),
            reading_id
        ))

        # Reject duplicate telemetry and its duplicate events.
        if cursor.rowcount == 0:

            print(
                f"DUPLICATE TELEMETRY SKIPPED: "
                f"{asset_id} | {reading_id[:12]}"
            )

            return False

        # Record newly detected alerts.
        for issue_id, issue in result["new_alerts"].items():

            cursor.execute("""
                INSERT INTO alert_history (
                    asset_id,
                    timestamp,
                    issue_id,
                    event_type,
                    severity,
                    message
                )
                VALUES (?, ?, ?, ?, ?, ?)
            """, (
                asset_id,
                timestamp,
                issue_id,
                "NEW",
                issue["severity"],
                issue["message"]
            ))

        # Record resolved alerts.
        for issue_id, issue in result["resolved_alerts"].items():

            cursor.execute("""
                INSERT INTO alert_history (
                    asset_id,
                    timestamp,
                    issue_id,
                    event_type,
                    severity,
                    message
                )
                VALUES (?, ?, ?, ?, ?, ?)
            """, (
                asset_id,
                timestamp,
                issue_id,
                "RESOLVED",
                issue["severity"],
                issue["message"]
            ))

    return True
