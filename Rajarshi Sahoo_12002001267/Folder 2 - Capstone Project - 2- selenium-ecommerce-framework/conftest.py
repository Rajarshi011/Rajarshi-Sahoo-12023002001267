"""Shared PyTest fixtures and failure screenshot integration."""

import sys
from pathlib import Path

import pytest


REPO_ROOT = Path(__file__).resolve().parent
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from pages.home_page import HomePage
from pages.login_page import LoginPage
from utils.config_reader import config
from utils.csv_reader import read_csv
from utils.driver_factory import DriverFactory
from utils.screenshot_utils import capture_screenshot


@pytest.fixture(scope="session")
def app_config():
    """Return the shared framework configuration."""
    return config


@pytest.fixture
def driver(app_config):
    """Create a browser for a test and close it during teardown."""
    browser = app_config.get("app", "browser")
    headless = app_config.get_bool("app", "headless")
    test_driver = DriverFactory.get_driver(browser, headless)
    yield test_driver
    test_driver.quit()


@pytest.fixture
def login_page(driver, app_config):
    """Return a login page object using the configured explicit wait."""
    return LoginPage(driver, app_config.get_int("timeouts", "explicit"))


@pytest.fixture
def home_page(driver, app_config):
    """Return a home page object using the configured explicit wait."""
    return HomePage(driver, app_config.get_int("timeouts", "explicit"))


@pytest.fixture(params=read_csv(config.test_data_dir + "/login_data.csv"))
def login_test_data(request):
    """Return one data-driven login row from the CSV file."""
    return request.param


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """Attach a failure screenshot to the pytest-html report."""
    outcome = yield
    report = outcome.get_result()
    if report.when == "call" and report.failed:
        driver = item.funcargs.get("driver")
        if driver is not None:
            path = capture_screenshot(driver, item.name)
            if path:
                try:
                    from pytest_html import extras
                    report.extras = getattr(report, "extras", [])
                    report.extras.append(extras.image(path))
                except Exception:
                    pass
