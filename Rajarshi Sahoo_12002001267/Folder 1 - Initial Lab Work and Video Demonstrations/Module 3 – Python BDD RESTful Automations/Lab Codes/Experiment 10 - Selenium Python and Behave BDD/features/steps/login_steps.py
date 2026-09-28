import os
import time

from behave import given, when, then
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


os.makedirs("screenshots", exist_ok=True)


@given("the user opens the SauceDemo website")
def open_website(context):
    context.driver.get("https://www.saucedemo.com/")
    time.sleep(2)

    context.driver.save_screenshot(
        "screenshots/01_login_page.png"
    )

    print("SauceDemo website opened successfully.")


@when("the user enters valid username and password")
def enter_credentials(context):
    wait = WebDriverWait(context.driver, 15)

    username = wait.until(
        EC.visibility_of_element_located(
            (By.ID, "user-name")
        )
    )
    username.send_keys("standard_user")
    time.sleep(2)

    password = context.driver.find_element(
        By.ID, "password"
    )
    password.send_keys("secret_sauce")
    time.sleep(2)

    context.driver.save_screenshot(
        "screenshots/02_credentials_entered.png"
    )

    print("Login credentials entered successfully.")


@when("the user clicks the login button")
def click_login(context):
    context.driver.find_element(
        By.ID, "login-button"
    ).click()

    time.sleep(2)

    print("Login button clicked.")


@then("the user should be redirected to the products page")
def verify_login(context):
    wait = WebDriverWait(context.driver, 15)

    wait.until(
        EC.visibility_of_element_located(
            (By.CLASS_NAME, "inventory_list")
        )
    )

    assert "/inventory.html" in context.driver.current_url

    context.driver.save_screenshot(
        "screenshots/03_products_page.png"
    )

    print("Login successful!")
    print("Products page verified.")