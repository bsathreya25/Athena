
from pathlib import Path
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from datetime import date

# -----------------------------------
# ATHENA DOCUMENTATION GENERATOR
# -----------------------------------

PROJECT = Path("ATHENA_Documentation")

# Create project directories
folders = [
    "screenshots",
    "docs",
    "presentation"
]

for folder in folders:
    (PROJECT / folder).mkdir(parents=True, exist_ok=True)


# -----------------------------------
# 1. CREATE README.md
# -----------------------------------

readme = """
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


# -----------------------------------
# 2. CREATE DOCUMENTATION FILES
# -----------------------------------

documents = {
    "TEST_RESULTS.md": """
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


# -----------------------------------
# 3. CREATE AI USAGE LOG
# -----------------------------------

ai_log = """
# ATHENA - AI Usage Log

| Date | AI Tool | Purpose | Human Verification |
|---|---|---|---|
| YYYY-MM-DD | ChatGPT | Documentation assistance | Pending |
| YYYY-MM-DD | Cursor | Code assistance | Pending |

Record actual AI usage and verification details.
"""

(PROJECT / "AI_USAGE_LOG.md").write_text(
    ai_log.strip() + "\n",
    encoding="utf-8"
)


# -----------------------------------
# 4. CREATE POWERPOINT PRESENTATION
# -----------------------------------

prs = Presentation()
prs.slide_width = Inches(13.33)
prs.slide_height = Inches(7.5)

slides = [
    (
        "ATHENA",
        ["Real-Time Fleet Intelligence Platform",
         "Hackathon Project Presentation"]
    ),
    (
        "Problem Statement",
        ["Challenges in monitoring vehicle conditions",
         "Need for reliable telemetry monitoring",
         "Importance of identifying abnormal readings"]
    ),
    (
        "Proposed Solution",
        ["ATHENA processes vehicle telemetry",
         "Monitors vehicle conditions",
         "Provides information through a dashboard"]
    ),
    (
        "System Architecture",
        ["Vehicle Data Generator",
         "Telemetry JSON",
         "Condense Pipeline",
         "ATHENA Backend",
         "ATHENA Dashboard"]
    ),
    (
        "Technologies Used",
        ["Python",
         "Condense",
         "Git and GitHub",
         "Add the actual frontend and database technologies"]
    ),
    (
        "Key Features",
        ["Real-time telemetry monitoring",
         "Vehicle condition monitoring",
         "Abnormal reading detection",
         "Alert generation",
         "Vehicle location tracking"]
    ),
    (
        "Application Screenshots",
        ["Insert genuine dashboard screenshot",
         "Insert genuine telemetry screenshot",
         "Insert genuine alert screenshot"]
    ),
    (
        "Testing and Results",
        ["Explain test scenarios",
         "Show actual test results",
         "Discuss bugs discovered and fixed"]
    ),
    (
        "Limitations and Future Scope",
        ["Mention current limitations",
         "Explain possible improvements"]
    ),
    (
        "Conclusion",
        ["ATHENA - Real-Time Fleet Intelligence",
         "Thank You"]
    )
]


def add_slide(title, points, cover=False):
    layout = prs.slide_layouts[6]
    slide = prs.slides.add_slide(layout)

    # Dark background
    background = slide.background.fill
    background.solid()
    background.fore_color.rgb = RGBColor(17, 24, 39)

    # Title
    title_box = slide.shapes.add_textbox(
        Inches(0.7), Inches(0.6),
        Inches(12), Inches(1.0)
    )
    title_frame = title_box.text_frame
    title_frame.text = title

    for paragraph in title_frame.paragraphs:
        paragraph.font.size = Pt(34 if cover else 30)
        paragraph.font.bold = True
        paragraph.font.color.rgb = RGBColor(34, 211, 166)

    # Content
    content_box = slide.shapes.add_textbox(
        Inches(1), Inches(2.0),
        Inches(11.3), Inches(4.7)
    )
    frame = content_box.text_frame
    frame.word_wrap = True

    for index, point in enumerate(points):
        paragraph = (
            frame.paragraphs[0]
            if index == 0 else frame.add_paragraph()
        )
        paragraph.text = ("• " if not cover else "") + point
        paragraph.font.size = Pt(25 if cover else 22)
        paragraph.font.color.rgb = RGBColor(240, 244, 248)
        paragraph.space_after = Pt(20)


for index, (title, points) in enumerate(slides):
    add_slide(title, points, cover=(index == 0))

presentation_path = (
    PROJECT / "presentation" / "ATHENA_Presentation.pptx"
)

prs.save(presentation_path)


# -----------------------------------
# 5. COMPLETION MESSAGE
# -----------------------------------

print("\n" + "=" * 45)
print(" ATHENA DOCUMENTATION CREATED SUCCESSFULLY")
print("=" * 45)

print("Project location:", PROJECT.resolve())
print("README:", PROJECT / "README.md")
print("Screenshots:", PROJECT / "screenshots")
print("Documentation:", PROJECT / "docs")
print("AI log:", PROJECT / "AI_USAGE_LOG.md")
print("Presentation:", presentation_path)

print("\nNext steps:")
print("1. Add genuine application screenshots.")
print("2. Update actual technologies and run commands.")
print("3. Enter verified test results.")
print("4. Add your team details.")
print("5. Review the presentation before submission.")

