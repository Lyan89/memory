from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
import time
import pyautogui, sys


def get_url(file_path="url.txt"):
    try:
        with open(file_path, "r") as file:
            url = file.readline().strip()
            return url
    except FileNotFoundError:
        print(f"Error: {file_path} not found.")
        return None

url = get_url()
print(url)

# Configure Chrome to capture browser logs
caps = DesiredCapabilities.CHROME
caps['goog:loggingPrefs'] = {'browser': 'ALL'}

options = Options()
options.add_experimental_option("detach", True)
options.set_capability("goog:loggingPrefs", {"browser": "ALL"})


# Open Window
driver = webdriver.Chrome(
    service=Service(ChromeDriverManager().install()),
    options=options
)
driver.maximize_window()
driver.get(url)
time.sleep(3)


pyautogui.moveTo(1266, 945)   # moves mouse
pyautogui.click()  # click the mouse





# Retrieve console logs after your click has been simulated.
logs = driver.get_log('browser')
for log_entry in logs:
    print(log_entry['message'])

print("finish")