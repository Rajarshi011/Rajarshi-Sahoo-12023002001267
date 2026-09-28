import os
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Create screenshot folder
os.makedirs("screenshots", exist_ok=True)

# Initialize browser
driver = webdriver.Chrome()
wait = WebDriverWait(driver, 15)

def pause():
    time.sleep(3)

def take_screenshot(filename):
    path = os.path.join("screenshots", filename)
    driver.save_screenshot(path)
    print("Screenshot saved:", path)

try:
    # Step 1: Open website
    driver.maximize_window()
    driver.get("https://demoqa.com/alerts")
    pause()

    # Scroll to the alert buttons
    alert_button = wait.until(
        EC.presence_of_element_located((By.ID, "alertButton"))
    )
    driver.execute_script(
        "arguments[0].scrollIntoView({block: 'center'});",
        alert_button
    )
    pause()

    take_screenshot("01_initial_page.png")

    # Step 2: Handle JavaScript Alert
    alert_button.click()
    alert = wait.until(EC.alert_is_present())

    print("Alert message:", alert.text)
    print("JavaScript alert is displayed.")

    # Pause to observe the alert
    pause()

    # Accept the alert
    alert.accept()
    pause()

    print("JavaScript Alert handled successfully!")

    # Step 3: Handle JavaScript Confirm - Accept
    confirm_button = wait.until(
        EC.element_to_be_clickable((By.ID, "confirmButton"))
    )
    confirm_button.click()

    confirm = wait.until(EC.alert_is_present())
    print("Confirm message:", confirm.text)

    # Pause to observe the confirmation dialog
    pause()

    confirm.accept()
    pause()

    result = wait.until(
        EC.visibility_of_element_located((By.ID, "confirmResult"))
    )

    assert result.text == "You selected Ok"
    print("JavaScript Confirm accepted successfully!")

    take_screenshot("02_confirm_accepted.png")

    # Step 4: Handle JavaScript Confirm - Dismiss
    confirm_button.click()
    confirm = wait.until(EC.alert_is_present())

    print("Confirmation dialog displayed again.")
    pause()

    confirm.dismiss()
    pause()

    result = wait.until(
        EC.visibility_of_element_located((By.ID, "confirmResult"))
    )

    assert result.text == "You selected Cancel"
    print("JavaScript Confirm dismissed successfully!")

    take_screenshot("03_confirm_dismissed.png")

    print("All tasks completed successfully!")

    # Keep browser open for observation
    pause()

finally:
    driver.quit()