"""PyTest product search coverage for the OpenCart demo store."""

import pytest

from utils.csv_reader import read_csv


@pytest.mark.search
class TestSearch:
    """Exercise valid, invalid, and counted product searches."""

    @staticmethod
    def _valid_search_term(app_config) -> str:
        """Return the first valid search term from the search CSV."""
        rows = read_csv(f"{app_config.test_data_dir}/search_data.csv")
        return next(row["search_term"] for row in rows if row["expected"] == "valid")

    def test_valid_product_search(self, home_page, app_config):
        """Verify a valid product search shows a matching result."""
        term = self._valid_search_term(app_config)
        home_page.load()
        results = home_page.search_product(term)
        assert "Search" in results.get_page_heading()
        assert results.is_product_present(term) is True

    def test_invalid_product_search(self, home_page):
        """Verify a nonsense product search displays the no-results message."""
        home_page.load()
        results = home_page.search_product("zzz_nonexistent_product_zzz")
        assert results.is_no_results_message_displayed() is True

    def test_search_result_count(self, home_page, app_config):
        """Verify a valid search returns at least one product."""
        term = self._valid_search_term(app_config)
        home_page.load()
        results = home_page.search_product(term)
        assert results.get_result_count() > 0
