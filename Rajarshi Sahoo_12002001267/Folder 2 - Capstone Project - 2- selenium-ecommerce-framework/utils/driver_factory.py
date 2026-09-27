"""WebDriver construction for supported browsers."""

from selenium import webdriver
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.edge.options import Options as EdgeOptions
from selenium.webdriver.firefox.options import Options as FirefoxOptions


class DriverFactory:
    """Create Selenium drivers using Selenium Manager."""

    @staticmethod
    def get_driver(browser: str = "chrome", headless: bool = False):
        """Return a configured Chrome, Firefox, or Edge WebDriver."""
        browser_name = browser.lower()

        if browser_name == "chrome":
            options = ChromeOptions()
            options.add_argument("--window-size=1920,1080")
            if headless:
                options.add_argument("--headless=new")
            return webdriver.Chrome(options=options)

        if browser_name == "firefox":
            options = FirefoxOptions()
            if headless:
                options.add_argument("-headless")
            return webdriver.Firefox(options=options)

        if browser_name == "edge":
            options = EdgeOptions()
            options.add_argument("--window-size=1920,1080")
            if headless:
                options.add_argument("--headless=new")
            return webdriver.Edge(options=options)

        raise ValueError(f"Unsupported browser: {browser}")
