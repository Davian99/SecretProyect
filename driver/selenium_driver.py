from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC # Wait for condition

def Driver(headless):
    options = webdriver.ChromeOptions()
    if headless:
        options.add_argument('--headless')

    options.add_argument('ignore-certificate-errors')
    options.add_argument("--window-size=1920,1080")
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option('useAutomationExtension', False)
    options.add_argument('log-level=3')

    driver = webdriver.Chrome(options=options)
    return driver
