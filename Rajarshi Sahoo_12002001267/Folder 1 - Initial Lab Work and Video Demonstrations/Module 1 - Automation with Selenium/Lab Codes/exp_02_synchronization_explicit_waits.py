from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Initialize Chrome WebDriver
driver = webdriver.Chrome()

try:
    # Maximize browser window
    driver.maximize_window()

    # Open the dynamic loading page
    driver.get(
        "https://the-internet.herokuapp.com/dynamic_loading/1"
    )

    # Locate the Start button
    start_button = driver.find_element(
        By.CSS_SELECTOR, "#start button"
    )

    # Click the Start button
    start_button.click()

    # Wait until the text becomes visible
    wait = WebDriverWait(driver, 15)

    result = wait.until(
        EC.visibility_of_element_located(
            (By.CSS_SELECTOR, "#finish h4")
        )
    )

    # Extract the displayed text
    actual_text = result.text

    # Verify the expected text
    assert actual_text == "Hello World!"

    # Display the result
    print("Text displayed:", actual_text)
    print("Synchronization successful!")

finally:
    # Close the browser
    driver.quit()