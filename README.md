
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



