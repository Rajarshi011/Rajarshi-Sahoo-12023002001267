from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class InventoryPage:

    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 15)

        self.inventory_list = (By.CLASS_NAME, "inventory_list")
        self.page_title = (By.CLASS_NAME, "title")

    def is_products_page_displayed(self):
        self.wait.until(
            EC.visibility_of_element_located(self.inventory_list)
        )
        return (
            "/inventory.html" in self.driver.current_url
            and self.driver.find_element(*self.page_title).text == "Products"
        )

    def get_page_title(self):
        title = self.wait.until(
            EC.visibility_of_element_located(self.page_title)
        )
        return title.text