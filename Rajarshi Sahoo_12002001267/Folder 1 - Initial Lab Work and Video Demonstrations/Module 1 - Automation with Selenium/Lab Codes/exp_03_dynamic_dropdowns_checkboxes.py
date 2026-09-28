import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Initialize Chrome WebDriver
driver = webdriver.Chrome()
driver.maximize_window()

wait = WebDriverWait(driver, 15)

try:
    # Open the Automation Practice website
    driver.get("https://rahulshettyacademy.com/AutomationPractice/")

    time.sleep(3)

    # -------------------------------
    # Task 1: Handle Multiple Checkboxes
    # -------------------------------

    checkboxes = wait.until(
        EC.presence_of_all_elements_located(
            (By.XPATH, "//input[@type='checkbox']")
        )
    )

    print("Total checkboxes:", len(checkboxes))

    # Select Option 1 and Option 3
    option1 = driver.find_element(
        By.XPATH, "//input[@value='option1']"
    )
    option3 = driver.find_element(
        By.XPATH, "//input[@value='option3']"
    )

    if not option1.is_selected():
        option1.click()

    time.sleep(3)

    if not option3.is_selected():
        option3.click()

    time.sleep(3)

    # Verify checkbox selection
    assert option1.is_selected()
    assert option3.is_selected()

    print("Option 1 selected:", option1.is_selected())
    print("Option 3 selected:", option3.is_selected())

    # -------------------------------
    # Task 2: Handle Autocomplete
    # -------------------------------

    autocomplete = wait.until(
        EC.visibility_of_element_located(
            (By.ID, "autocomplete")
        )
    )

    autocomplete.clear()
    autocomplete.send_keys("Ind")

    time.sleep(3)

    # Locate autocomplete suggestions
    suggestions = wait.until(
        EC.visibility_of_all_elements_located(
            (By.CSS_SELECTOR, ".ui-autocomplete li")
        )
    )

    print("Autocomplete suggestions:")
    for suggestion in suggestions:
        print(suggestion.text)

    # Select India from the suggestions
    india_found = False

    for suggestion in suggestions:
        if suggestion.text.strip().casefold() == "india":
            suggestion.click()
            india_found = True
            break

    assert india_found, "India suggestion not found"

    time.sleep(3)

    # Verify the selected country
    selected_country = autocomplete.get_attribute("value")

    assert selected_country == "India"

    print("Selected country:", selected_country)
    print("All tasks completed successfully!")

finally:
    driver.quit()