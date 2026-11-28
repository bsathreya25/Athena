
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
| Section | Written form |
|---|---|
| Module description | This module simulates vehicle telemetry for ATHENA. It generates CAN-like and GPS data for a fleet and supports repeatable fault scenarios for testing and demonstrations. |
| Imports | The module uses Python libraries for command-line arguments, JSON, random values, timing, HTTP requests, UTC timestamps, file paths, and type annotations. |
| Fleet hub coordinates | It defines five representative Indian fleet hubs: Bengaluru, Mumbai, Delhi, Hyderabad, and Pune. Each hub is represented by latitude and longitude. |
| Supported scenarios | The generator supports normal operation, high temperature, critical overheating, low voltage, missing data, invalid values, and mixed scenarios. |
| UTC timestamp helper | The helper returns the current UTC date and time in ISO 8601 format, ending in `Z`. |



| Section | Written form |
|---|---|
| Module purpose | Defines ATHENA’s canonical vehicle telemetry schema, validation rules, and rule evaluation. |
| Imports | Uses future annotations, Python’s date/time parser, and `Any` for flexible field-specification types. |
| `vehicle_id` | Required text field identifying the vehicle. Unit: ID. |
| `timestamp` | Required text field containing a timestamp in ISO 8601 format. |
| `engine_temp_c` | Required numeric field for engine temperature. Valid range: −40°C to 200°C. |
| `vehicle_speed_kmh` | Required numeric field for vehicle speed. Valid range: 0 to 260 km/h. |
| `battery_voltage_v` | Required numeric field for battery voltage. Valid range: 0 to 36 V. |
| `fuel_level_pct` | Required numeric field for fuel level. Valid range: 0% to 100%. |
| `rpm` | Required numeric field for engine RPM. The excerpt ends before its range or unit is shown. |



| Part | Written description |
|---|---|
| Purpose | Inspects generated vehicle telemetry stored as JSON or JSON Lines and checks its schema and alert accuracy. |
| Imports | Uses command-line argument handling, JSON processing, a counter for tallying results, file paths, and flexible data types. It also uses ATHENA’s telemetry classifier. |
| Record loading | Reads a file as UTF-8 text. An empty file produces an empty list of records. |
| JSON Lines handling | For a JSON Lines file, parses each non-empty line as a separate record. |
| JSON handling | For a standard JSON file, keeps each item when the file contains an array; if it contains one object, wraps that object in a list. |
| Record inspection | Classifies each record, counts how many records have each severity, and counts issues by their type. It also prepares a list for flagged records. |
| Excerpt limit | The provided excerpt ends while processing issues, so it doesn’t show how flagged records are populated or what summary is returned. |



| Test | Written description |
|---|---|
| Sample payload severity checks | Loads the sample payload cases and checks that each one receives its expected severity. Each case is reported separately if it fails. |
| Normal generator scenario | Generates telemetry for 5 vehicles over 3 rounds, expecting 15 records. It verifies each record is valid and classified as normal. |
| Critical overheating scenario | Generates telemetry for 3 vehicles over 2 rounds and checks that every generated record is classified as critical. |
| Mixed batch inspector | Generates a mixed batch for 10 vehicles over 5 rounds and passes it to the inspector. The excerpt ends before showing what inspection results are checked. |


| Case | Written description |
|---|---|
| TC-01 — Normal operation | Vehicle ATH-001 reports an engine temperature of 85°C, speed of 54.5 km/h, battery voltage of 13.6 volts, fuel level of 72%, and engine speed of 2,150 RPM. Its GPS coordinates are in Bengaluru, and it has no diagnostic trouble codes. Expected severity: normal. |
| TC-02 — High engine temperature | Vehicle ATH-002 reports an engine temperature of 99.5°C, speed of 48 km/h, battery voltage of 13.4 volts, fuel level of 65%, and engine speed of 2,900 RPM. Its GPS coordinates are also in Bengaluru, and it has no diagnostic trouble codes. Expected severity: warning. |
| TC-03 — Critical temperature and cooling stress | Vehicle ATH-003 reports an engine temperature of 112°C, speed of 12 km/h, battery voltage of 13.1 volts, and fuel level of 58%. The case is expected to be critical. The provided excerpt ends before showing the remaining fields. |



| Test case | Temperature | Voltage | Generated status |
|---|---:|---:|---|
| TC01 - Normal | 28 | 5.0 | NORMAL |
| TC02 - Normal | 32 | 4.8 | NORMAL |
| TC03 - High Temperature | 42 | 5.0 | HIGH TEMPERATURE WARNING |
| TC04 - Critical Temperature | 65 | 5.0 | CRITICAL ALERT |
| TC05 - Low Voltage | 30 | 2.5 | LOW VOLTAGE WARNING |
| TC06 - High Temp + Low Voltage | 45 | 2.5 | HIGH TEMPERATURE WARNING |
| TC07 - Missing Temperature | None | 5.0 | ERROR: DATA MISSING |
| TC08 - Missing Voltage | 30 | None | ERROR: DATA MISSING |
| TC09 - Invalid Temperature | -200 | 5.0 | ERROR: INVALID SENSOR VALUE |
| TC10 - Invalid Voltage | 30 | -5.0 | ERROR: INVALID SENSOR VALUE |
| TC11 - Empty Input | None | None | ERROR: DATA MISSING |
| TC12 - Extreme Temperature | 100 | 5.0 | CRITICAL ALERT |



