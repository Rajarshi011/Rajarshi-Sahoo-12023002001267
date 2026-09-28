import os
import time
import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Create folders if they do not exist
os.makedirs("screenshots", exist_ok=True)
os.makedirs("reports", exist_ok=True)


@pytest.fixture
def driver():
    browser = webdriver.Chrome()
    browser.maximize_window()
    yield browser
    browser.quit()


def login(driver, username, password, screenshot_name):
    driver.get("https://www.saucedemo.com/")
    time.sleep(2)

    # Screenshot 1: Login page
    if username == "standard_user":
        driver.save_screenshot("screenshots/01_login_page.png")

    wait = WebDriverWait(driver, 15)

    # Enter username
    wait.until(
        EC.visibility_of_element_located((By.ID, "user-name"))
    ).send_keys(username)

    # Enter password
    driver.find_element(By.ID, "password").send_keys(password)
    time.sleep(2)

    # Screenshot: Entered credentials
    driver.save_screenshot(
        f"screenshots/{screenshot_name}_credentials.png"
    )

    # Click login
    driver.find_element(By.ID, "login-button").click()
    time.sleep(2)


def test_successful_login(driver):
    login(driver, "standard_user", "secret_sauce", "02")

    wait = WebDriverWait(driver, 15)
    wait.until(
        EC.visibility_of_element_located(
            (By.CLASS_NAME, "inventory_list")
        )
    )

    assert "/inventory.html" in driver.current_url

    # Screenshot 3: Successful login
    driver.save_screenshot("screenshots/03_successful_login.png")
    print("Successful login test passed.")
    time.sleep(2)


def test_invalid_login(driver):
    login(driver, "invalid_user", "wrong_password", "04")

    wait = WebDriverWait(driver, 15)
    error = wait.until(
        EC.visibility_of_element_located(
            (By.CSS_SELECTOR, "h3[data-test='error']")
        )
    )

    assert "Username and password do not match" in error.text

    # Screenshot 5: Invalid login error
    driver.save_screenshot("screenshots/05_invalid_login_error.png")
    print("Invalid login test passed.")
    time.sleep(2)


def test_locked_out_user(driver):
    login(driver, "locked_out_user", "secret_sauce", "06")

    wait = WebDriverWait(driver, 15)
    error = wait.until(
        EC.visibility_of_element_located(
            (By.CSS_SELECTOR, "h3[data-test='error']")
        )
    )

    assert "locked out" in error.text

    # Screenshot 7: Locked-out user error
    driver.save_screenshot("screenshots/07_locked_out_error.png")
    print("Locked-out user test passed.")
    time.sleep(2)