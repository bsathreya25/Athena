
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
Ask User
Completed with input: {
  "message": "Do you mean improve the formatting of the tables I’ve written here, or implement a visual redesign for tables in the ATHENA dashboard?",
  "requestedSchema": {
    "properties": {
      "target": {
        "type": "string",
        "title": "Table target",
        "oneOf": [
          {
            "const": "chat",
            "title": "Polish the tables in this conversation"
          },
          {
            "const": "dashboard",
            "title": "Implement the redesign in the ATHENA dashboard"
          }
        ]
      }
    }
  }
}

Here’s a cleaner, consistent layout for the tables in this conversation.

### ATHENA generator

| Component | Purpose | Details |
|---|---|---|
| Module | Simulates vehicle telemetry | Generates CAN-like and GPS data for fleet testing and demonstrations. |
| Fleet hubs | Provides sample GPS locations | Bengaluru, Mumbai, Delhi, Hyderabad, and Pune. |
| Scenarios | Simulates operating conditions | Normal, high temperature, critical overheating, low voltage, missing data, invalid values, and mixed. |
| Timestamp helper | Creates event timestamps | Uses the current time in UTC and ISO 8601 format. |

### ATHENA telemetry schema

| Field | Required? | Accepted values |
|---|---:|---|
| Vehicle ID | Yes | Text identifier |
| Timestamp | Yes | ISO 8601 text |
| Engine temperature | Yes | −40°C to 200°C |
| Vehicle speed | Yes | 0 to 260 km/h |
| Battery voltage | Yes | 0 to 36 V |
| Fuel level | Yes | 0% to 100% |
| RPM | Yes | Numeric; the provided excerpt doesn’t show its range or unit. |

### ATHENA inspector

| Step | What it does |
|---|---|
| Read input | Loads a JSON or JSON Lines file. |
| Handle empty files | Returns an empty list when the file has no content. |
| Parse JSON Lines | Treats each non-empty line as a separate record. |
| Parse JSON | Uses each array item as a record, or wraps a single object as one record. |
| Inspect records | Classifies each record and counts severity levels and issue types. |
| Excerpt limit | The provided code ends before showing the final summary or flagged-record handling. |

### ATHENA unit tests

| Test | Verification |
|---|---|
| Sample payloads | Each sample receives its expected severity. |
| Normal generation | Five vehicles over three rounds produce 15 valid records, all classified as normal. |
| Critical overheating | Every record generated for three vehicles over two rounds is classified as critical. |
| Mixed batch | A mixed batch for 10 vehicles over five rounds is inspected; the excerpt doesn’t show the assertions. |

### ATHENA sample payloads

| Case | Scenario | Key values | Expected severity |
|---|---|---|---|
| TC-01 | Normal operation | 85°C; 54.5 km/h; 13.6 V; 72% fuel; 2,150 RPM; no diagnostic codes | NORMAL |
| TC-02 | High engine temperature | 99.5°C; 48 km/h; 13.4 V; 65% fuel; 2,900 RPM; no diagnostic codes | WARNING |
| TC-03 | Critical temperature and cooling stress | 112°C; 12 km/h; 13.1 V; 58% fuel. Remaining fields aren’t shown in the excerpt. | CRITICAL |

### VIGILANT test results

| Case | Temperature | Voltage | Result |
|---|---:|---:|---|
| TC01 — Normal | 28 | 5.0 | NORMAL |
| TC02 — Normal | 32 | 4.8 | NORMAL |
| TC03 — High temperature | 42 | 5.0 | HIGH TEMPERATURE WARNING |
| TC04 — Critical temperature | 65 | 5.0 | CRITICAL ALERT |
| TC05 — Low voltage | 30 | 2.5 | LOW VOLTAGE WARNING |
| TC06 — High temperature and low voltage | 45 | 2.5 | HIGH TEMPERATURE WARNING |
| TC07 — Missing temperature | Missing | 5.0 | ERROR: DATA MISSING |
| TC08 — Missing voltage | 30 | Missing | ERROR: DATA MISSING |
| TC09 — Invalid temperature | −200 | 5.0 | ERROR: INVALID SENSOR VALUE |
| TC10 — Invalid voltage | 30 | −5.0 | ERROR: INVALID SENSOR VALUE |
| TC11 — Empty input | Missing | Missing | ERROR: DATA MISSING |
| TC12 — Extreme temperature | 100 | 5.0 | CRITICAL ALERT |



