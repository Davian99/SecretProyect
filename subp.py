import subprocess
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
#other imports

subprocess.Popen(
   '"C:\\Program Files (x86)\\Google\\Chrome\\Application\\chrome.exe" --remote-debugging-port=9222', shell=True)


options = webdriver.ChromeOptions()
options.add_experimental_option("debuggerAddress", "127.0.0.1:9222")

driver = webdriver.Chrome(options=options)
#driver.maximize_window()
driver.get('https://www.bet365.com')
