from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import os


# Create screenshots folder
os.makedirs("screenshots", exist_ok=True)


# Page Object Model: Login Page
class LoginPage:

    def __init__(self, driver):
        self.driver = driver
        self.username = (By.ID, "user-name")
        self.password = (By.ID, "password")
        self.login_button = (By.ID, "login-button")

    def enter_username(self, username):
        self.driver.find_element(*self.username).send_keys(username)

    def enter_password(self, password):
        self.driver.find_element(*self.password).send_keys(password)

    def click_login(self):
        self.driver.find_element(*self.login_button).click()


# Page Object Model: Inventory Page
class InventoryPage:

    def __init__(self, driver):
        self.driver = driver
        self.inventory_title = (By.CLASS_NAME, "title")

    def get_page_title(self):
        return WebDriverWait(self.driver, 15).until(
            EC.visibility_of_element_located(self.inventory_title)
        ).text


# Main Test Execution
driver = webdriver.Chrome()
wait = WebDriverWait(driver, 15)

try:
    driver.maximize_window()

    # Open the website
    driver.get("https://www.saucedemo.com/")
    print("SauceDemo website opened successfully.")
    time.sleep(3)

    # Create LoginPage object
    login_page = LoginPage(driver)

    # Capture initial login page
    driver.save_screenshot("screenshots/01_login_page.png")
    print("Screenshot 1: Login page saved.")

    # Enter login credentials
    login_page.enter_username("standard_user")
    time.sleep(3)

    login_page.enter_password("secret_sauce")
    time.sleep(3)

    # Capture entered credentials
    driver.save_screenshot("screenshots/02_login_credentials.png")
    print("Screenshot 2: Login credentials entered.")

    # Click login button
    login_page.click_login()
    print("Login button clicked.")
    time.sleep(3)

    # Create InventoryPage object
    inventory_page = InventoryPage(driver)

    # Verify successful login
    page_title = inventory_page.get_page_title()
    assert page_title == "Products", "Login verification failed!"

    # Capture inventory page
    driver.save_screenshot("screenshots/03_inventory_page.png")
    print("Screenshot 3: Inventory page saved.")

    print("Page title:", page_title)
    print("Page Object Model automation successful!")

finally:
    driver.quit()
    print("Browser closed successfully.")