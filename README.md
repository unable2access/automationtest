# Rev's Automated UI Tests

Simple Selenium-based test runner that exercises a few pages on a site and generates an HTML report with screenshots.

## Overview
- Runs a set of scenarios (navigation, search, social links, intentional fail).
- Saves output inside `Generated Report/` and screenshots in `Generated Report/screenshots/`.
- HTML report is created inside `Generated Report/`.

## Prerequisites
- Python 3.8+
- Google Chrome installed

## Install
Optional: create a virtual environment:
- Windows:
  - python -m venv .venv
  - .venv\Scripts\activate

Dependencies:
- If `requirements.txt` exists:
  - pip install -r requirements.txt
- Minimal dependencies:
  - selenium
  - webdriver-manager

## Run
- Execute the test script:
  - python Run.py

## Outputs
- HTML report: `Generated Report/Test_Report_<timestamp>.html`
- Screenshots: `Generated Report/screenshots/*.png`
- Console prints per-scenario results and a failed/error summary.

## Notes
- `webdriver-manager` will download the correct ChromeDriver automatically.
- Virtual environment is optional but recommended to avoid global package conflicts.