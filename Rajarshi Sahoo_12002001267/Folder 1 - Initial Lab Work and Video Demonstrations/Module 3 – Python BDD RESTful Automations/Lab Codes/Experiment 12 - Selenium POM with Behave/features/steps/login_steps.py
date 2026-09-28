import time

from behave import given, when, then
from pages.login_page import LoginPage
from pages.inventory_page import InventoryPage


@given("the user opens the SauceDemo website")
def open_website(context):
    context.login_page = LoginPage(context.driver)
    context.login_page.open_website()

    time.sleep(3)
    context.driver.save_screenshot(
        "screenshots/01_login_page.png"
    )

    print("SauceDemo website opened successfully.")
    print("Screenshot 1: Login page saved.")


@when("the user enters valid login credentials")
def enter_credentials(context):
    context.login_page.enter_username("standard_user")
    time.sleep(3)

    context.login_page.enter_password("secret_sauce")
    time.sleep(3)

    context.driver.save_screenshot(
        "screenshots/02_login_credentials.png"
    )

    print("Login credentials entered successfully.")
    print("Screenshot 2: Login credentials saved.")


@when("the user clicks the login button")
def click_login(context):
    context.login_page.click_login()

    time.sleep(3)
    print("Login button clicked.")


@then("the user should be redirected to the products page")
def verify_products_page(context):
    context.inventory_page = InventoryPage(context.driver)

    assert context.inventory_page.is_products_page_displayed(), (
        "Products page was not displayed."
    )

    time.sleep(2)
    context.driver.save_screenshot(
        "screenshots/03_products_page.png"
    )

    print("Products page verified successfully.")
    print("Screenshot 3: Products page saved.")
    print("Page title:", context.inventory_page.get_page_title())
    print("Page Object Model with Behave executed successfully!")