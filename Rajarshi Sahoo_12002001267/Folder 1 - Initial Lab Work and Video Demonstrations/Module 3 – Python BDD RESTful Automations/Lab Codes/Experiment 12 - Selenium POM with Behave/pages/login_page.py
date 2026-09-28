import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class LoginPage:

    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 15)

        self.username_field = (By.ID, "user-name")
        self.password_field = (By.ID, "password")
        self.login_button = (By.ID, "login-button")

    def open_website(self):
        self.driver.get("https://www.saucedemo.com/")
        self.wait.until(
            EC.visibility_of_element_located(self.username_field)
        )

    def enter_username(self, username):
        username_input = self.wait.until(
            EC.visibility_of_element_located(self.username_field)
        )
        username_input.send_keys(username)

    def enter_password(self, password):
        password_input = self.wait.until(
            EC.visibility_of_element_located(self.password_field)
        )
        password_input.send_keys(password)

    def click_login(self):
        login = self.wait.until(
            EC.element_to_be_clickable(self.login_button)
        )
        login.click()