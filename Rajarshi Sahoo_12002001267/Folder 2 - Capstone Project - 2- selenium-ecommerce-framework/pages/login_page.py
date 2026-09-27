"""Page object for the OpenCart login page."""

from selenium.webdriver.common.by import By

from pages.base_page import BasePage
from utils.config_reader import config


class LoginPage(BasePage):
    """Represent the account login page and its authentication actions."""

    EMAIL_FIELD = (By.ID, "input-email")
    PASSWORD_FIELD = (By.ID, "input-password")
    LOGIN_BUTTON = (By.CSS_SELECTOR, "input.btn.btn-primary[value='Login']")
    WARNING_ALERT = (By.CSS_SELECTOR, ".alert.alert-danger")
    MY_ACCOUNT_LINK = (By.LINK_TEXT, "My Account")

    def load(self) -> None:
        """Open the configured account login page."""
        self.open(f"{config.get_base_url()}index.php?route=account/login")

    def enter_email(self, email: str) -> None:
        """Enter an email address into the login form."""
        self.type(self.EMAIL_FIELD, email)

    def enter_password(self, password: str) -> None:
        """Enter a password into the login form."""
        self.type(self.PASSWORD_FIELD, password)

    def click_login(self) -> None:
        """Submit the login form."""
        self.click(self.LOGIN_BUTTON)

    def login(self, email: str, password: str) -> None:
        """Enter credentials and submit the login form."""
        self.enter_email(email)
        self.enter_password(password)
        self.click_login()

    def get_warning_message(self) -> str:
        """Return the visible login warning text."""
        return self.get_text(self.WARNING_ALERT)

    def is_login_successful(self) -> bool:
        """Return whether the account URL or My Account marker confirms login."""
        return self.wait_for_url_contains("route=account/account") or self.is_visible(
            self.MY_ACCOUNT_LINK
        )

    def is_error_displayed(self) -> bool:
        """Return whether the login danger alert is visible."""
        return self.is_visible(self.WARNING_ALERT)
