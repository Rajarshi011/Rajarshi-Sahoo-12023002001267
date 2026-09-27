"""Gate 4 - live locator + page-object verification for the tutorialsninja framework.

Run from the repo root with the venv active:   python gate4_check.py
"""
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from utils.config_reader import config
from utils.driver_factory import DriverFactory
from utils.csv_reader import read_csv
from pages.login_page import LoginPage
from pages.home_page import HomePage

TIMEOUT = config.get_int("timeouts", "explicit")
PROBE_TERM = "MacBook"
NONSENSE = "zzz_nonexistent_product_zzz"


def step(name, fn, nonempty=False):
    """Run one check, print PASS/FAIL, never abort the whole run."""
    try:
        value = fn()
    except Exception as exc:  # report the failing locator and continue
        print(f"[FAIL] {name} -> {type(exc).__name__}: {str(exc)[:150]}")
        return False
    if nonempty and not value:
        print(f"[FAIL] {name} -> empty result")
        return False
    shown = "" if value in (None, "") else f" -> {str(value)[:120]}"
    print(f"[PASS] {name}{shown}")
    return True


def main():
    driver = DriverFactory.get_driver(
        config.get("app", "browser"), config.get_bool("app", "headless")
    )
    ok = []
    try:
        login = LoginPage(driver, TIMEOUT)

        print("\n--- 1) Login page locators ---")
        ok.append(step("open login page", login.load))
        ok.append(step("type into email field", lambda: login.enter_email("probe@test.com")))
        ok.append(step("type into password field", lambda: login.enter_password("probe123")))
        ok.append(step("click login button", login.click_login))
        ok.append(step("invalid login -> warning alert", login.get_warning_message, nonempty=True))

        print("\n--- 2) Valid login (CSV row 1) ---")
        row = read_csv(ROOT / "test_data" / "login_data.csv")[0]
        email = (row.get("email") or "").strip()
        password = (row.get("password") or "").strip()
        if not email or email == "demo.user@example.com":
            print("[SKIP] CSV row 1 still has the placeholder email. Register a demo "
                  "account, paste it into test_data/login_data.csv, then re-run.")
        else:
            login.load()
            login.login(email, password)
            ok.append(step("valid login succeeds", login.is_login_successful))

        print("\n--- 3) Product search via POM ---")
        home = HomePage(driver, TIMEOUT)
        home.load()
        results = home.search_product(PROBE_TERM)
        ok.append(step("search page heading", results.get_page_heading, nonempty=True))
        ok.append(step("product titles found", results.get_result_titles, nonempty=True))
        ok.append(step(f"'{PROBE_TERM}' present in results",
                       lambda: results.is_product_present(PROBE_TERM)))

        print("\n--- 4) Negative search ---")
        home.load()
        empty = home.search_product(NONSENSE)
        ok.append(step("no-results message shown",
                       empty.is_no_results_message_displayed))
    finally:
        print("\nClosing browser...")
        driver.quit()

    print("\n================ RESULT ================")
    print(f"{sum(ok)}/{len(ok)} checks passed (see any FAIL/SKIP above)")


if __name__ == "__main__":
    main()
