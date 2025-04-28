from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities

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

driver = webdriver.Chrome(
    service=Service(ChromeDriverManager().install()),
    options=options
)

driver.get(url)

# Wait until the canvas is present (max 20 seconds)
canvas = WebDriverWait(driver, 20).until(
    EC.presence_of_element_located((By.TAG_NAME, "canvas"))
)

# Find canvas
canvas = driver.find_element(By.TAG_NAME, "canvas")

# Get canvas size
canvas_width = canvas.size['width']
canvas_height = canvas.size['height']
print(f"Canvas size: {canvas_width}x{canvas_height}")

from selenium.webdriver.common.action_chains import ActionChains

# Assume the interactive element is already located
interactive_div = driver.find_element(By.CLASS_NAME, "c3htmlwrap")


# Retrieve console logs after your click has been simulated.
logs = driver.get_log('browser')
for log_entry in logs:
    print(log_entry['message'])