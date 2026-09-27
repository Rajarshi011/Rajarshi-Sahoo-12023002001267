# Selenium Python E-Commerce Framework

## Overview

This project is a browser automation framework for the [TutorialsNinja OpenCart demo store](https://tutorialsninja.com/demo/). It demonstrates a maintainable Selenium test structure using:

- Page Object Model (POM)
- Selenium WebDriver with Chrome, Firefox, and Edge support
- PyTest fixtures, markers, and HTML reporting
- Python `unittest` coverage for comparison and compatibility
- CSV-driven test data
- Explicit waits and configurable timeouts
- Automatic screenshots for failed PyTest tests
- A live locator and page-object verification script

The tests cover account login and product search, including positive, negative, empty-input, and data-driven cases.

## Requirements

- Python 3.10 or newer
- A supported browser: Google Chrome, Mozilla Firefox, or Microsoft Edge
- Internet access to reach the demo store
- A registered TutorialsNinja account for the valid-login tests

Selenium 4.6 and newer uses Selenium Manager to obtain the appropriate browser driver automatically. A separate driver download is normally not required.

## Installation

Open PowerShell in the project root and run:

```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -r requirements.txt
```

If PowerShell blocks script activation, activate the environment through Command Prompt instead:

```cmd
venv\Scripts\activate.bat
```

To verify the installation without opening a browser:

```powershell
pytest --collect-only
```

## Configuration

All runtime settings are in `config/config.ini`:

```ini
[app]
base_url = https://tutorialsninja.com/demo/
browser = chrome
headless = false
demo_pause = 3.0
implicit_wait = 5

[timeouts]
explicit = 10
```

Important settings:

| Setting | Purpose | Examples |
| --- | --- | --- |
| `app.base_url` | Store URL used by the page objects | `https://tutorialsninja.com/demo/` |
| `app.browser` | Browser selected by `DriverFactory` | `chrome`, `firefox`, `edge` |
| `app.headless` | Run without a visible browser window | `true` or `false` |
| `app.demo_pause` | Optional pause used by page actions | `0`, `1.0`, `3.0` |
| `timeouts.explicit` | Maximum wait for expected page conditions | `10` |

Set the valid account under `[credentials]` before running the successful-login tests. Keep credentials out of source control in a shared or production environment.

## Running the Tests

Run the complete PyTest suite. The default settings in `pytest.ini` also create a self-contained HTML report:

```powershell
pytest
```

Run only a test group with the registered markers:

```powershell
pytest -m login
pytest -m search
```

Run a specific suite or file:

```powershell
pytest tests/pytest_tests/test_login_pytest.py
pytest tests/pytest_tests/test_search_pytest.py
```

Run the independent `unittest` login suite:

```powershell
python -m unittest discover -s tests/unittest_tests -p "test_*.py" -v
```

Run the live Gate 4 verification script. It opens one browser and checks login locators, a valid login, product search, and a no-results search:

```powershell
python gate4_check.py
```

## Test Coverage

### PyTest login tests

- Valid credentials reach the account page
- Invalid credentials display an error
- Empty credentials display an error
- Every row in `test_data/login_data.csv` is executed as a parameterized case

### PyTest search tests

- Valid product searches show matching results
- Invalid searches show the no-results message
- Valid searches return at least one product

### Unittest login tests

The `unittest` suite repeats the core login scenarios using `setUp` and `tearDown` instead of PyTest fixtures.

## Test Data

The CSV files use headers and are read as dictionaries:

- `test_data/login_data.csv`: `email`, `password`, `expected`, and `case`
- `test_data/search_data.csv`: `search_term`, `expected`, and `case`

To add a login case, add a row with `expected` set to `success` or `error`. To add a search case, add a row with `expected` set to `valid` or `invalid`. The current search tests select the first row marked `valid` and separately use a fixed nonsense term for the negative test.

## Project Structure

```text
selenium-ecommerce-framework/
├── config/config.ini              Runtime URL, browser, waits, and credentials
├── pages/                         Page Object Model classes
│   ├── base_page.py               Shared navigation, waits, and actions
│   ├── home_page.py               Store home page and search
│   ├── login_page.py              Account login page
│   └── search_results_page.py     Search result assertions and locators
├── tests/
│   ├── pytest_tests/              PyTest login and search tests
│   └── unittest_tests/            Python unittest login tests
├── test_data/                     CSV test inputs
├── utils/
│   ├── config_reader.py           Configuration access
│   ├── csv_reader.py              CSV loading helpers
│   ├── driver_factory.py          Browser creation
│   ├── logger.py                  File and console logging
│   └── screenshot_utils.py        Timestamped failure screenshots
├── conftest.py                    Shared PyTest fixtures and report hooks
├── gate4_check.py                 Live locator/POM smoke verification
├── pytest.ini                     Discovery, markers, and report options
├── requirements.txt               Python dependencies
├── reports/                       HTML reports and run logs
└── screenshots/                   Captured screenshots from failed tests
```

## Framework Design

1. Tests request fixtures such as `driver`, `login_page`, and `home_page`.
2. `DriverFactory` creates the configured browser and Selenium Manager resolves its driver.
3. Page classes hide locators and browser actions from test code.
4. `BasePage` centralizes waits and common interactions.
5. CSV helpers provide repeatable data-driven inputs.
6. The PyTest hook captures a screenshot when a browser test fails and attaches it to the HTML report.

## Reports and Troubleshooting

- PyTest HTML report: `reports/report.html`
- Framework log: `reports/run.log`
- Failure screenshots: `screenshots/`

Generated reports and screenshots are ignored by Git, except for their `.gitkeep` files.

Common issues:

- **Browser does not start:** confirm the browser is installed and try `browser = chrome`, `firefox`, or `edge`.
- **Valid login fails:** register an account on the demo site and update both `[credentials]` in `config/config.ini` and the success row in `test_data/login_data.csv`.
- **Element or timeout failures:** check internet access, increase `timeouts.explicit`, and confirm the demo site is available.
- **Tests run too slowly for local debugging:** set `app.demo_pause = 0` and `app.headless = true`.
- **Unexpected stale results:** delete the generated files in `reports/` and `screenshots/`, then rerun the tests.

## Dependencies

Dependencies are pinned by minimum compatible versions in `requirements.txt`:

- Selenium
- PyTest
- pytest-html
- Faker
