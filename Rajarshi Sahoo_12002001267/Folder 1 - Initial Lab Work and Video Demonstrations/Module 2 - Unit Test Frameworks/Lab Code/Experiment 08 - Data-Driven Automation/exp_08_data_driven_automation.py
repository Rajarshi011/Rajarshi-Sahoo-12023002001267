import csv
import os
import time

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


os.makedirs("screenshots", exist_ok=True)
from pathlib import Path

CSV_FILE = Path(__file__).resolve().parent / "test_data.csv"
BASE_URL = "https://www.saucedemo.com/"

with open(CSV_FILE, mode="r", newline="", encoding="utf-8") as file:
    test_cases = list(csv.DictReader(file))

for index, test_case in enumerate(test_cases, start=1):
    username = test_case["username"]
    password = test_case["password"]
    expected_result = test_case["expected_result"]

    driver = webdriver.Chrome()
    wait = WebDriverWait(driver, 15)

    try:
        driver.maximize_window()
        driver.get(BASE_URL)
        print(f"\nTest Case {index}: {username}")
        print("SauceDemo website opened successfully.")
        time.sleep(3)

        username_field = wait.until(
            EC.visibility_of_element_located((By.ID, "user-name"))
        )
        username_field.send_keys(username)
        time.sleep(3)

        password_field = driver.find_element(By.ID, "password")
        password_field.send_keys(password)
        time.sleep(3)

        driver.save_screenshot(
            f"screenshots/08_test_case_{index}_login.png"
        )
        print(f"Screenshot {index}: Login details saved.")

        login_button = driver.find_element(By.ID, "login-button")
        login_button.click()
        time.sleep(3)

        if expected_result == "success":
            wait.until(
                EC.visibility_of_element_located(
                    (By.CLASS_NAME, "inventory_list")
                )
            )

            assert "/inventory.html" in driver.current_url
            print("Actual result: Login successful.")
            print("Test status: PASS")

        else:
            error_message = wait.until(
                EC.visibility_of_element_located(
                    (By.CSS_SELECTOR, "h3[data-test='error']")
                )
            ).text

            assert error_message != ""
            print("Actual result: Login failed as expected.")
            print("Error message:", error_message)
            print("Test status: PASS")

        driver.save_screenshot(
            f"screenshots/08_test_case_{index}_result.png"
        )
        print(f"Screenshot {index}: Test result saved.")

    except Exception as error:
        print("Test status: FAIL")
        print("Error:", error)

        driver.save_screenshot(
            f"screenshots/08_test_case_{index}_failure.png"
        )

    finally:
        driver.quit()
        print("Browser closed successfully.")
        time.sleep(2)

print("\nData-driven automation completed.")