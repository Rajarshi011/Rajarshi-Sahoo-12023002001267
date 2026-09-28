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
    # Step 1: Open and maximize browser
    driver.maximize_window()
    driver.get("https://rahulshettyacademy.com/AutomationPractice/")
    time.sleep(2)

    # Step 2: Locate the web table
    table = wait.until(
        EC.presence_of_element_located((By.ID, "product"))
    )

    # Scroll to the table
    driver.execute_script(
        "arguments[0].scrollIntoView({block: 'center'});",
        table
    )
    time.sleep(2)

    # Screenshot 1: Initial table
    driver.save_screenshot(
        "screenshots/01_initial_web_table.png"
    )
    print("Screenshot 1: Initial table saved.")

    # Step 3: Extract table headers
    headers = table.find_elements(By.CSS_SELECTOR, "th")
    header_names = [header.text.strip() for header in headers]

    print("\nTable Headers:")
    print(header_names)

    # Step 4: Locate table rows
    rows = table.find_elements(By.CSS_SELECTOR, "tbody tr")
    extracted_data = []

    print("\nStarting row-by-row extraction...")

    # Step 5: Highlight and extract each row
    for index, row in enumerate(rows[1:], start=1):

        # Scroll to the current row
        driver.execute_script(
            "arguments[0].scrollIntoView({block: 'center'});",
            row
        )

        # Highlight the current row
        driver.execute_script("""
            arguments[0].style.backgroundColor = 'yellow';
            arguments[0].style.outline = '3px solid red';
        """, row)

        # Extract cell data
        cells = row.find_elements(By.CSS_SELECTOR, "td")
        row_data = [cell.text.strip() for cell in cells]

        if row_data:
            extracted_data.append(row_data)
            print(f"Row {index}: {row_data}")

        # Keep the highlight visible for 1 second
        time.sleep(1)

        # Remove highlight before processing the next row
        driver.execute_script("""
            arguments[0].style.backgroundColor = '';
            arguments[0].style.outline = '';
        """, row)

    # Step 6: Verify extracted data
    assert header_names, "Table headers not found!"
    assert extracted_data, "No table records found!"

    print("\nTotal records extracted:", len(extracted_data))
    print("HTML Web Table extraction successful!")

    # Screenshot 2: Final table
    driver.save_screenshot(
        "screenshots/02_extracted_web_table.png"
    )
    print("Screenshot 2: Extracted table saved.")

    # Step 7: Briefly display the final result
    time.sleep(2)

finally:
    # Step 8: Automatically close browser
    driver.quit()
    print("Browser closed successfully.")