
# ATHENA - Real-Time Fleet Intelligence Platform

## Project Overview
ATHENA is a fleet-intelligence platform designed to monitor
vehicle telemetry, identify abnormal vehicle conditions and
provide useful information for fleet monitoring.

## Problem Statement
Fleet operators need a reliable way to monitor vehicle
conditions and identify potential issues using vehicle data.

## Proposed Solution
ATHENA processes vehicle telemetry and presents relevant
information through a monitoring dashboard.

## Key Features
- Real-time vehicle telemetry monitoring
- Vehicle condition monitoring
- Abnormal reading detection
- Alert generation
- Vehicle location tracking
- Sensor data validation

> Verify each feature against the working application.

## System Architecture

Vehicle Data Generator
        |
        v
Telemetry JSON
        |
        v
Condense Pipeline
        |
        v
ATHENA Backend
        |
        v
ATHENA Dashboard

## Technologies Used
- Python
- Condense
- Git
- GitHub
- Frontend framework: To be confirmed
- Database: To be confirmed

## Installation

Clone the repository:

```bash
git clone YOUR_GITHUB_REPOSITORY_URL
```

Install dependencies:

```bash
pip install -r requirements.txt
```

## Running the Application

Add the verified backend and frontend startup commands here.

## Testing and Validation

| Test | Expected Result | Actual Result | Status |
|---|---|---|---|
| Normal temperature | Normal status | Pending | Not tested |
| High temperature | Warning alert | Pending | Not tested |
| Critical temperature | Critical alert | Pending | Not tested |
| Low voltage | Voltage warning | Pending | Not tested |
| Missing telemetry | Missing-data handling | Pending | Not tested |
| Invalid telemetry | Validation error | Pending | Not tested |

## Screenshots

See the screenshots folder for genuine application screenshots.

## Known Limitations
- To be documented after testing.

## Future Improvements
- Improved telemetry validation
- Better alert handling
- Improved dashboard visualisation

## Team Contributions
Add team members and their responsibilities here.

## AI Usage Disclosure
Document AI tools used and how their output was reviewed.

## License
Add the approved project license here.
"""

(PROJECT / "README.md").write_text(readme, encoding="utf-8")

# 2. CREATE DOCUMENTATION FILES
# ATHENA Test Results

| Test Scenario | Expected Result | Actual Result | Status |
|---|---|---|---|
| Normal temperature | Normal status | Pending | Not tested |
| High temperature | Warning alert | Pending | Not tested |
| Critical temperature | Critical alert | Pending | Not tested |
| Low voltage | Voltage warning | Pending | Not tested |
| Missing data | Proper error handling | Pending | Not tested |
| Invalid values | Validation error | Pending | Not tested |

Update actual results only after running each test.
""",

    "KNOWN_LIMITATIONS.md": """
# ATHENA Known Limitations

Record limitations discovered during development and testing.

## Current Limitations
- To be updated after testing.

## Known Bugs
- To be updated after testing.

## Future Improvements
- Improved telemetry validation.
- Improved alert handling.
- Additional monitoring capabilities.
""",

    "ARCHITECTURE.md": """
# ATHENA Architecture

Vehicle Data Generator
        |
        v
Telemetry JSON
        |
        v
Condense Pipeline
        |
        v
Backend
        |
        v
Dashboard

Verify this diagram against the actual implementation.
""",

    "DEMO_SCRIPT.md": """
# ATHENA Demonstration Script

1. Introduce ATHENA.
2. Explain the problem being solved.
3. Show the application dashboard.
4. Demonstrate live telemetry.
5. Demonstrate an alert using a real test scenario.
6. Explain the testing results.
7. Discuss limitations and future improvements.
"""
}

for filename, content in documents.items():
    (PROJECT / "docs" / filename).write_text(
        content.strip() + "\n",
        encoding="utf-8"
    )



# 3. CREATE AI USAGE LOG



# ATHENA - AI Usage Log
"""Canonical vehicle telemetry schema, validation, and rule evaluation for ATHENA."""

from __future__ import annotations

import math
from datetime import datetime
from typing import Any

# Physical validity bounds used to spot corrupted, missing, or impossible sensor values.
FIELD_SPECS: dict[str, dict[str, Any]] = {
    "vehicle_id": {"type": (str,), "required": True, "unit": "id"},
    "timestamp": {"type": (str,), "required": True, "unit": "iso8601"},
    "engine_temp_c": {
        "type": (int, float),
        "required": True,
        "min": -40.0,
        "max": 200.0,
        "unit": "°C",
    },
    "vehicle_speed_kmh": {
        "type": (int, float),
        "required": True,
        "min": 0.0,
        "max": 260.0,
        "unit": "km/h",
    },
    "battery_voltage_v": {
        "type": (int, float),
        "required": True,
        "min": 0.0,
        "max": 36.0,
        "unit": "V",
    },
    "fuel_level_pct": {
        "type": (int, float),
        "required": True,
        "min": 0.0,
        "max": 100.0,
        "unit": "%",
    },
    "rpm": {
        "type": (int, float),
        "required": True,
        "min": 0.0,
        "max": 10_000.0,
        "unit": "rpm",
    },
}

SEVERITY_ORDER = {"info": 0, "warning": 1, "critical": 2}


def _is_number(value: Any) -> bool:
    """Return whether value is a finite numeric value (excluding booleans)."""
    return (
        isinstance(value, (int, float))
        and not isinstance(value, bool)
        and math.isfinite(value)
    )


def _parse_timestamp(value: str) -> datetime | None:
    """Parse an ISO-8601 timestamp, accepting a trailing Z for UTC."""
    normalized = value[:-1] + "+00:00" if value.endswith("Z") else value
    try:
        return datetime.fromisoformat(normalized)
    except ValueError:
        return None


def validate_telemetry(payload: Any) -> list[str]:
    """Validate a telemetry payload and return all validation error messages.

    Unknown fields are allowed so payloads can carry additional metadata.
    """
    if not isinstance(payload, dict):
        return ["Payload must be a JSON object."]

    errors: list[str] = []

    for field, spec in FIELD_SPECS.items():
        if field not in payload:
            if spec["required"]:
                errors.append(f"Missing required field: {field}.")
            continue

        value = payload[field]
        expected_types = spec["type"]

        if expected_types == (int, float):
            if not _is_number(value):
                errors.append(f"{field} must be a finite number.")
                continue
        elif not isinstance(value, expected_types):
            expected = " or ".join(t.__name__ for t in expected_types)
            errors.append(f"{field} must be of type {expected}.")
            continue

        if field == "vehicle_id" and not value.strip():
            errors.append("vehicle_id must not be empty.")

        if field == "timestamp":
            if not value.strip():
                errors.append("timestamp must not be empty.")
            elif _parse_timestamp(value) is None:
                errors.append("timestamp must be a valid ISO-8601 datetime.")

        if _is_number(value):
            minimum = spec.get("min")
            maximum = spec.get("max")
            if minimum is not None and value < minimum:
                errors.append(f"{field} must be at least {minimum} {spec['unit']}.")
            if maximum is not None and value > maximum:
                errors.append(f"{field} must be at most {maximum} {spec['unit']}.")

    return errors


def evaluate_rules(payload: Any) -> list[dict[str, str]]:
    """Evaluate operational thresholds and return alert dictionaries.

    Each alert has ``code``, ``field``, ``severity``, and ``message`` keys.
    Invalid or absent values are skipped; use :func:`validate_telemetry`
    to report payload problems.
    """
    if not isinstance(payload, dict):
        return []

    alerts: list[dict[str, str]] = []

    def add_alert(
        code: str, field: str, severity: str, message: str
    ) -> None:
        alerts.append(
            {
                "code": code,
                "field": field,
                "severity": severity,
                "message": message,
            }
        )

    engine_temp = payload.get("engine_temp_c")
    if _is_number(engine_temp):
        if engine_temp >= 125:
            add_alert(
                "ENGINE_OVERHEAT",
                "engine_temp_c",
                "critical",
                f"Engine temperature is critically high ({engine_temp} °C).",
            )
        elif engine_temp >= 110:
            add_alert(
                "ENGINE_TEMP_HIGH",
                "engine_temp_c",
                "warning",
                f"Engine temperature is high ({engine_temp} °C).",
            )

    battery_voltage = payload.get("battery_voltage_v")
    if _is_number(battery_voltage):
        if battery_voltage < 11:
            add_alert(
                "BATTERY_CRITICAL",
                "battery_voltage_v",
                "critical",
                f"Battery voltage is critically low ({battery_voltage} V).",
            )
        elif battery_voltage < 12:
            add_alert(
                "BATTERY_LOW",
                "battery_voltage_v",
                "warning",
                f"Battery voltage is low ({battery_voltage} V).",
            )

    fuel_level = payload.get("fuel_level_pct")
    if _is_number(fuel_level):
        if fuel_level <= 5:
            add_alert(
                "FUEL_CRITICAL",
                "fuel_level_pct",
                "critical",
                f"Fuel level is critically low ({fuel_level}%).",
            )
        elif fuel_level <= 10:
            add_alert(
                "FUEL_LOW",
                "fuel_level_pct",
                "warning",
                f"Fuel level is low ({fuel_level}%).",
            )

    rpm = payload.get("rpm")
    if _is_number(rpm):
        if rpm >= 6_500:
            add_alert(
                "RPM_CRITICAL",
                "rpm",
                "critical",
                f"Engine RPM is critically high ({rpm} rpm).",
            )
        elif rpm >= 5_500:
            add_alert(
                "RPM_HIGH",
                "rpm",
                "warning",
                f"Engine RPM is high ({rpm} rpm).",
            )

    alerts.sort(key=lambda alert: SEVERITY_ORDER[alert["severity"]], reverse=True)
    return alerts


def classify_severity(payload: Any) -> str:
    """Return the highest alert severity, or ``info`` when there are no alerts."""
    alerts = evaluate_rules(payload)
    if not alerts:
        return "info"
    return max(alerts, key=lambda alert: SEVERITY_ORDER[alert["severity"]])["severity"]
    """Inspect generated telemetry JSON/JSONL records for schema and alert accuracy."""

from __future__ import annotations

import argparse
import json
from collections import Counter
from pathlib import Path
from typing import Any

from telemetry.schema import classify_telemetry


def load_records(path: Path) -> list[Any]:
    """Load telemetry records from a .json (object or array) or .jsonl file."""
    raw = path.read_text(encoding="utf-8").strip()
    if not raw:
        return []

    if path.suffix.lower() == ".jsonl":
        records = []
        for line_number, line in enumerate(raw.splitlines(), start=1):
            if not line.strip():
                continue
            try:
                records.append(json.loads(line))
            except json.JSONDecodeError as exc:
                raise ValueError(
                    f"Invalid JSON on line {line_number} of {path}: {exc.msg}"
                ) from exc
        return records

    parsed = json.loads(raw)
    if isinstance(parsed, list):
        return parsed
    return [parsed]


def inspect_records(records: list[Any]) -> dict[str, Any]:
    """Validate and classify every record and return a structured inspection summary."""
    severity_counts: Counter[str] = Counter()
    issue_counts: Counter[str] = Counter()
    flagged_records: list[dict[str, Any]] = []

    for index, record in enumerate(records):
        result = classify_telemetry(record)
        severity = str(result.get("severity", "unknown"))
        issues = result.get("issues", [])

        if not isinstance(issues, list):
            issues = [str(issues)]

        severity_counts[severity] += 1

        for issue in issues:
            issue_type = str(issue).split(":", 1)[0].strip()
            issue_counts[issue_type or "unknown"] += 1

        if issues or severity.strip().lower() not in {
            "normal",
            "ok",
            "healthy",
            "none",
        }:
            flagged_records.append(
                {
                    "index": index,
                    "severity": severity,
                    "issues": issues,
                    "record": record,
                }
            )

    return {
        "records_inspected": len(records),
        "severity_counts": dict(sorted(severity_counts.items())),
        "issue_counts": dict(sorted(issue_counts.items())),
        "flagged_records": flagged_records,
    }


def main() -> int:
    """Run the inspector CLI and print a JSON inspection summary."""
    parser = argparse.ArgumentParser(
        description="Inspect telemetry records from a JSON or JSONL file."
    )
    parser.add_argument("input", type=Path, help="Path to the input .json or .jsonl file")
    args = parser.parse_args()

    try:
        records = load_records(args.input)
        summary = inspect_records(records)
    except (OSError, json.JSONDecodeError, ValueError) as exc:
        parser.error(str(exc))

    print(json.dumps(summary, indent=2, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
    """Unit tests for ATHENA telemetry generation, validation, and alert classification."""

from __future__ import annotations

import json
import unittest
from pathlib import Path

from generator.telemetry_generator import generate_batch
from telemetry.inspector import inspect_records
from telemetry.schema import classify_telemetry, validate_record


class TelemetryTests(unittest.TestCase):
    def test_sample_payloads_match_expected_severities(self) -> None:
        payloads_path = Path(__file__).parent / "sample_payloads.json"
        cases = json.loads(payloads_path.read_text(encoding="utf-8"))

        for case in cases:
            with self.subTest(case_id=case["case_id"]):
                result = classify_telemetry(case["payload"])
                self.assertEqual(result["severity"], case["expected_severity"])

    def test_generator_normal_scenario_produces_valid_records(self) -> None:
        events = generate_batch(
            vehicle_count=5,
            rounds=3,
            scenario="normal",
            seed=42,
        )
        self.assertEqual(len(events), 15)

        for event in events:
            self.assertEqual(validate_record(event), [])
            self.assertEqual(classify_telemetry(event)["severity"], "NORMAL")

    def test_generator_critical_overheat_triggers_critical(self) -> None:
        events = generate_batch(
            vehicle_count=3,
            rounds=2,
            scenario="critical_overheat",
            seed=7,
        )

        for event in events:
            result = classify_telemetry(event)
            self.assertEqual(result["severity"], "CRITICAL")

    def test_inspector_summarizes_mixed_batch(self) -> None:
        events = generate_batch(
            vehicle_count=10,
            rounds=5,
            scenario="mixed",
            seed=99,
        )

        summary = inspect_records(events)
        self.assertIsNotNone(summary)


if __name__ == "__main__":
    unittest.main()
    [
  {
    "case_id": "TC-01",
    "description": "Normal operating telemetry",
    "expected_severity": "NORMAL",
    "payload": {
      "vehicle_id": "ATH-001",
      "timestamp": "2026-11-28T01:00:00Z",
      "engine_temp_c": 85.0,
      "vehicle_speed_kmh": 54.5,
      "battery_voltage_v": 13.6,
      "fuel_level_pct": 72.0,
      "rpm": 2150,
      "gps": {
        "lat": 12.9716,
        "lon": 77.5946
      },
      "dtc_codes": []
    }
  },
  {
    "case_id": "TC-02",
    "description": "High engine temperature warning",
    "expected_severity": "WARNING",
    "payload": {
      "vehicle_id": "ATH-002",
      "timestamp": "2026-11-28T01:00:05Z",
      "engine_temp_c": 99.5,
      "vehicle_speed_kmh": 48.0,
      "battery_voltage_v": 13.4,
      "fuel_level_pct": 65.0,
      "rpm": 2900,
      "gps": {
        "lat": 12.9751,
        "lon": 77.5982
      },
      "dtc_codes": []
    }
  }
]

| Date | AI Tool | Purpose | Human Verification |
|---|---|---|---|
| YYYY-MM-DD | ChatGPT | Documentation assistance | Pending |
| YYYY-MM-DD | Cursor | Code assistance | Pending |

