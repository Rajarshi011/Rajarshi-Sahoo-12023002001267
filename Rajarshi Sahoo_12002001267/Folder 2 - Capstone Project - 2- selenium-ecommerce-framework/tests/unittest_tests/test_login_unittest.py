"""Unittest login coverage for the OpenCart demo store."""

import unittest

from pages.login_page import LoginPage
from utils.config_reader import config
from utils.driver_factory import DriverFactory


class TestLoginUnittest(unittest.TestCase):
    """Exercise login flows without PyTest fixtures."""

    def setUp(self) -> None:
        """Create a browser and login page before each test."""
        self.driver = DriverFactory.get_driver(
            config.get("app", "browser"),
            config.get_bool("app", "headless"),
        )
        self.login_page = LoginPage(
            self.driver,
            config.get_int("timeouts", "explicit"),
        )

    def tearDown(self) -> None:
        """Close the browser after each test."""
        self.driver.quit()

    def test_valid_login(self) -> None:
        """Verify configured credentials reach the account page."""
        self.login_page.load()
        self.login_page.login(
            config.get("credentials", "valid_email"),
            config.get("credentials", "valid_password"),
        )
        self.assertTrue(self.login_page.is_login_successful())

    def test_invalid_login(self) -> None:
        """Verify invalid credentials display a warning."""
        self.login_page.load()
        self.login_page.login("wrong@example.com", "wrongpass")
        self.assertTrue(self.login_page.is_error_displayed())
        self.assertNotEqual(self.login_page.get_warning_message().strip(), "")

    def test_empty_credentials(self) -> None:
        """Verify empty credentials display an error."""
        self.login_page.load()
        self.login_page.login("", "")
        self.assertTrue(self.login_page.is_error_displayed())


if __name__ == "__main__":
    unittest.main()
