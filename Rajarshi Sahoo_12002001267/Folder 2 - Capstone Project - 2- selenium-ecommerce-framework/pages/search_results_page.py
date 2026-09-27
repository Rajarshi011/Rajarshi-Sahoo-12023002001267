"""Page object for OpenCart product search results."""

from selenium.webdriver.common.by import By

from pages.base_page import BasePage


class SearchResultsPage(BasePage):
    """Represent the product search results page."""

    PAGE_HEADING = (By.CSS_SELECTOR, "#content h1")
    RESULT_TITLES = (By.CSS_SELECTOR, ".product-layout .caption h4 a")
    NO_RESULTS_MESSAGE = (
        By.XPATH,
        "//p[contains(normalize-space(), 'There is no product that matches the search criteria.')]")

    def get_page_heading(self) -> str:
        """Return the search results heading."""
        return self.get_text(self.PAGE_HEADING)

    def get_result_titles(self) -> list[str]:
        """Return visible product title strings from the result cards."""
        return [element.text for element in self.find_all(self.RESULT_TITLES)]

    def get_result_count(self) -> int:
        """Return the number of product titles in the current results."""
        return len(self.get_result_titles())

    def is_product_present(self, product_name: str) -> bool:
        """Return whether a result title contains the requested product name."""
        expected = product_name.casefold()
        return any(expected in title.casefold() for title in self.get_result_titles())

    def is_no_results_message_displayed(self) -> bool:
        """Return whether the standard no-results message is visible."""
        return self.is_visible(self.NO_RESULTS_MESSAGE)

    def open_product(self, product_name: str) -> None:
        """Open the first result whose title contains the requested product name."""
        expected = product_name.casefold()
        for element in self.find_all(self.RESULT_TITLES):
            if expected in element.text.casefold():
                element.click()
                return
        raise ValueError(f"Product not found in search results: {product_name}")
