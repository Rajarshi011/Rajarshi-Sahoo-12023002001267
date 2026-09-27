"""Shared explicit-wait browser actions for page objects."""

from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import TimeoutException

from utils.screenshot_utils import capture_screenshot
import time
from utils.config_reader import config


class BasePage:
    """Provide reusable Selenium operations for all page objects."""

    def __init__(self, driver, timeout: int = 10) -> None:
        """Initialize the page object with a driver and explicit wait timeout."""
        self.driver = driver
        self.wait = WebDriverWait(self.driver, timeout)

        try:
            self.pause = config.get_float("app", "demo_pause")
        except Exception:
            self.pause = 0.0

    def open(self, url: str) -> None:
        """Navigate the browser to a URL."""
        self.driver.get(url)
        self._pause()

    def find(self, locator: tuple[str, str]):
        """Return the first element present for a locator."""
        return self.wait.until(EC.presence_of_element_located(locator))

    def find_all(self, locator: tuple[str, str]) -> list:
        """Return all elements present for a locator."""
        return self.wait.until(EC.presence_of_all_elements_located(locator))

    def click(self, locator: tuple[str, str]) -> None:
        """Wait for a locator to be clickable and click its element."""
        self.wait.until(EC.element_to_be_clickable(locator)).click()
        self._pause()

    def type(self, locator: tuple[str, str], text: str) -> None:
        """Clear a visible field and type text into it."""
        element = self.wait.until(EC.visibility_of_element_located(locator))
        element.clear()
        element.send_keys(text)
        self._pause()

    def get_text(self, locator: tuple[str, str]) -> str:
        """Return the text of a visible element."""
        return self.wait.until(EC.visibility_of_element_located(locator)).text

    def is_visible(self, locator: tuple[str, str], timeout: int | None = None) -> bool:
        """Return whether a locator becomes visible before the timeout."""
        try:
            wait = WebDriverWait(self.driver, timeout) if timeout is not None else self.wait
            wait.until(EC.visibility_of_element_located(locator))
            return True
        except TimeoutException:
            return False

    def wait_for_url_contains(self, fragment: str) -> bool:
        """Wait until the browser URL contains a fragment and return the result."""
        return self.wait.until(EC.url_contains(fragment))

    def get_current_url(self) -> str:
        """Return the browser's current URL."""
        return self.driver.current_url

    def get_title(self) -> str:
        """Return the current browser page title."""
        return self.driver.title

    def take_screenshot(self, name: str) -> str | None:
        """Capture a screenshot using the framework screenshot helper."""
        return capture_screenshot(self.driver, name)

    def _pause(self):
        """Optional slow-motion pause for live observation (demo_pause in config.ini)."""
        if self.pause:
            time.sleep(self.pause)
