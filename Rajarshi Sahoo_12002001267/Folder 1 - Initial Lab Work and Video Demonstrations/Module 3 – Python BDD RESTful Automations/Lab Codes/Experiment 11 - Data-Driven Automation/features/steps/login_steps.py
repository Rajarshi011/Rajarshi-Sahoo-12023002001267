import csv
import os
import time

from behave import given, when, then
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


SCREENSHOT_DIR = os.path.join("screenshots")
os.makedirs(SCREENSHOT_DIR, exist_ok=True)


@given("the user opens the SauceDemo website")
def open_website(context):
    context.driver.get("https://www.saucedemo.com/")
    time.sleep(2)

    context.driver.save_screenshot(
        os.path.join(SCREENSHOT_DIR, "01_login_page.png")
    )

    print("SauceDemo website opened successfully.")


@when("the user performs login tests using the CSV data")
def perform_login_tests(context):
    csv_path = os.path.join(
        "test_data", "login_data.csv"
    )

    with open(csv_path, newline="", encoding="utf-8") as file:
        test_cases = list(csv.DictReader(file))

    context.results = []

    for index, test_case in enumerate(test_cases, start=1):
        username = test_case["username"]
        password = test_case["password"]
        expected = test_case["expected_result"]

        driver = context.driver
        wait = WebDriverWait(driver, 15)

        # Open the login page for each test case
        driver.get("https://www.saucedemo.com/")

        # Enter username
        username_field = wait.until(
            EC.visibility_of_element_located(
                (By.ID, "user-name")
            )
        )
        username_field.send_keys(username)

        # Enter password
        password_field = driver.find_element(
            By.ID, "password"
        )
        password_field.send_keys(password)

        time.sleep(2)

        # Capture credentials screenshot
        driver.save_screenshot(
            os.path.join(
                SCREENSHOT_DIR,
                f"{index:02d}_{username}_credentials.png"
            )
        )

        # Click login button
        driver.find_element(By.ID, "login-button").click()
        time.sleep(2)

        # Verify the expected result
        if expected == "success":
            wait.until(
                EC.visibility_of_element_located(
                    (By.CLASS_NAME, "inventory_list")
                )
            )

            actual = (
                "success"
                if "/inventory.html" in driver.current_url
                else "error"
            )

        else:
            error_message = wait.until(
                EC.visibility_of_element_located(
                    (By.CLASS_NAME, "error-message-container")
                )
            )

            actual = (
                "error"
                if error_message.is_displayed()
                else "success"
            )

        # Capture result screenshot
        driver.save_screenshot(
            os.path.join(
                SCREENSHOT_DIR,
                f"{index:02d}_{username}_result.png"
            )
        )

        passed = actual == expected

        context.results.append({
            "username": username,
            "expected": expected,
            "actual": actual,
            "passed": passed
        })

        print(
            f"Test {index}: {username} | "
            f"Expected: {expected} | "
            f"Actual: {actual} | "
            f"{'PASS' if passed else 'FAIL'}"
        )


@then("all login test cases should produce the expected results")
def verify_results(context):
    assert context.results, "No test cases were executed."

    failed_tests = [
        result for result in context.results
        if not result["passed"]
    ]

    total = len(context.results)
    passed = total - len(failed_tests)

    print("\nData-Driven Test Summary")
    print("------------------------")
    print(f"Total test cases: {total}")
    print(f"Passed: {passed}")
    print(f"Failed: {len(failed_tests)}")

    assert not failed_tests, (
        f"{len(failed_tests)} test case(s) failed."
    )

    print("All data-driven login tests passed!")