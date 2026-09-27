"""Page object for the OpenCart home page."""

from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By

from pages.base_page import BasePage
from utils.config_reader import config


class HomePage(BasePage):
    """Represent the store home page and its header search."""

    SEARCH_BOX = (By.NAME, "search")
    SEARCH_BUTTON = (By.CSS_SELECTOR, "#search button")
    SEARCH_BUTTON_FALLBACK = (By.ID, "button-search")

    def load(self) -> None:
        """Open the configured store home page."""
        self.open(config.get_base_url())

    def search_product(self, term: str):
        """Search for a term and return the resulting page object."""
        from pages.search_results_page import SearchResultsPage

        self.type(self.SEARCH_BOX, term)
        try:
            self.click(self.SEARCH_BUTTON)
        except TimeoutException:
            self.click(self.SEARCH_BUTTON_FALLBACK)
        return SearchResultsPage(self.driver, self.wait._timeout)
