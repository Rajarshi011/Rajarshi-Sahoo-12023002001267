from selenium import webdriver
from selenium.webdriver.common.by import By
import time

# Initialize Chrome WebDriver
driver = webdriver.Chrome()
time.sleep(3)

# Maximize browser window
driver.maximize_window()
time.sleep(3)

# Open the web application
driver.get("https://www.saucedemo.com/")
time.sleep(3)

# Enter username using ID locator
username = driver.find_element(By.ID, "user-name")
time.sleep(3)
username.send_keys("standard_user")
time.sleep(3)

# Enter password using NAME locator
password = driver.find_element(By.NAME, "password")
time.sleep(3)
password.send_keys("secret_sauce")
time.sleep(3)

# Locate login button using XPATH locator
login_button = driver.find_element(
    By.XPATH, "//input[@type='submit']"
)
time.sleep(3)

# Click login button
login_button.click()
time.sleep(3)

# Verify successful login
current_url = driver.current_url
time.sleep(3)

assert "/inventory.html" in current_url

print("Login successful!")
print("Current URL:", current_url)
time.sleep(3)

# Close the browser
driver.quit()