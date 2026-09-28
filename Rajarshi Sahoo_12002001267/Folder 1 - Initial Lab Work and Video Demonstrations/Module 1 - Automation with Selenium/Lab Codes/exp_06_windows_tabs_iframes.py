from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import os

# Create screenshots folder
os.makedirs("screenshots", exist_ok=True)

# Initialize WebDriver
driver = webdriver.Chrome()
wait = WebDriverWait(driver, 20)

try:
    # Step 1: Open DemoQA Browser Windows page
    driver.maximize_window()
    driver.get("https://demoqa.com/browser-windows")
    time.sleep(3)

    main_window = driver.current_window_handle
    print("Main window opened successfully.")

    # Step 2: Open a new tab
    new_tab_button = wait.until(
        EC.element_to_be_clickable((By.ID, "tabButton"))
    )
    new_tab_button.click()

    wait.until(EC.number_of_windows_to_be(2))

    # Switch to the new tab
    for handle in driver.window_handles:
        if handle != main_window:
            driver.switch_to.window(handle)
            break

    time.sleep(3)
    print("Switched to new tab.")
    print("Tab title:", driver.title)

    # Verify new tab content
    tab_heading = wait.until(
        EC.visibility_of_element_located((By.ID, "sampleHeading"))
    )
    assert tab_heading.text == "This is a sample page"

    driver.save_screenshot("screenshots/01_new_tab.png")
    print("Screenshot 1: New tab saved.")

    # Close new tab and return to main window
    driver.close()
    driver.switch_to.window(main_window)
    print("Returned to main window.")
    time.sleep(3)

    # Step 3: Open a new browser window
    new_window_button = wait.until(
        EC.element_to_be_clickable((By.ID, "windowButton"))
    )
    new_window_button.click()

    wait.until(EC.number_of_windows_to_be(2))

    # Switch to the new window
    for handle in driver.window_handles:
        if handle != main_window:
            driver.switch_to.window(handle)
            break

    time.sleep(3)
    print("Switched to new window.")
    print("Window title:", driver.title)

    # Verify new window content
    window_heading = wait.until(
        EC.visibility_of_element_located((By.ID, "sampleHeading"))
    )
    assert window_heading.text == "This is a sample page"

    driver.save_screenshot("screenshots/02_new_window.png")
    print("Screenshot 2: New window saved.")

    # Close new window and return to main window
    driver.close()
    driver.switch_to.window(main_window)
    print("Returned to main window.")
    time.sleep(3)

    # Step 4: Open the iframe practice page
    driver.get("https://demo.automationtesting.in/Frames.html")
    time.sleep(3)

    # Locate the single iframe
    iframe = wait.until(
        EC.presence_of_element_located((By.ID, "singleframe"))
    )

    # Scroll to iframe
    driver.execute_script(
        "arguments[0].scrollIntoView({block: 'center'});",
        iframe
    )
    time.sleep(3)

    # Step 5: Switch into the iframe
    driver.switch_to.frame(iframe)
    print("Switched to iframe successfully.")

    # Locate the input field inside the iframe
    input_field = wait.until(
        EC.visibility_of_element_located(
            (By.CSS_SELECTOR, "input[type='text']")
        )
    )

    # Enter text into the iframe
    input_field.send_keys("Selenium iframe automation successful!")
    print("Text entered into iframe successfully.")

    time.sleep(3)

    # Capture screenshot while inside iframe
    driver.save_screenshot("screenshots/03_iframe_content.png")
    print("Screenshot 3: Iframe content saved.")

    # Step 6: Return to the main page
    driver.switch_to.default_content()
    print("Returned to main page from iframe.")

    time.sleep(3)
    driver.save_screenshot("screenshots/04_main_page.png")
    print("Screenshot 4: Main page saved.")

    print("Windows, tabs, and iframe handling successful!")

finally:
    # Step 7: Close browser automatically
    driver.quit()
    print("Browser closed successfully.")