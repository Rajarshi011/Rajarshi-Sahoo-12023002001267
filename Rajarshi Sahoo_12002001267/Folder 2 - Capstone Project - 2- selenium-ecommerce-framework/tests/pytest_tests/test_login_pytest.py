"""PyTest login coverage for the OpenCart demo store."""

import pytest


@pytest.mark.login
class TestLogin:
    """Exercise valid, invalid, empty, and data-driven login cases."""

    def test_valid_login(self, login_page, app_config):
        """Verify configured credentials reach the account page."""
        login_page.load()
        login_page.login(
            app_config.get("credentials", "valid_email"),
            app_config.get("credentials", "valid_password"),
        )
        assert login_page.is_login_successful() is True

    def test_invalid_login(self, login_page):
        """Verify invalid credentials display a warning message."""
        login_page.load()
        login_page.login("wrong@example.com", "wrongpass")
        assert login_page.is_error_displayed() is True
        assert login_page.get_warning_message().strip()

    def test_empty_credentials(self, login_page):
        """Verify submitting blank credentials displays an error."""
        login_page.load()
        login_page.login("", "")
        assert login_page.is_error_displayed() is True

    def test_data_driven_login(self, login_page, login_test_data):
        """Verify each CSV login row produces its expected outcome."""
        login_page.load()
        login_page.login(login_test_data["email"], login_test_data["password"])
        if login_test_data["expected"] == "success":
            assert login_page.is_login_successful() is True
        else:
            assert login_page.is_error_displayed() is True
