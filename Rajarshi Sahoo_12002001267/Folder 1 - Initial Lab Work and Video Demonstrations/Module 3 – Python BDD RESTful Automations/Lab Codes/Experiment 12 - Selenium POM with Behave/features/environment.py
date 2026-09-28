from selenium import webdriver
import os


def before_scenario(context, scenario):
    os.makedirs("screenshots", exist_ok=True)

    context.driver = webdriver.Chrome()
    context.driver.maximize_window()


def after_scenario(context, scenario):
    if hasattr(context, "driver"):
        context.driver.quit()
        print("Browser closed successfully.")