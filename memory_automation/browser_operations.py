from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
import time



class Browser:
    def __init__(self, headless=False, detach=True, logging=True):
        self.headless = headless
        self.detach = detach
        self.logging = logging
        self.driver = self._init_driver()

    def _init_driver(self):
        caps = DesiredCapabilities.CHROME.copy()
        if self.logging:
            caps['goog:loggingPrefs'] = {'browser': 'ALL'}

        options = Options()
        if self.headless:
            options.add_argument('--headless')
        if self.detach:
            options.add_experimental_option("detach", True)
        if self.logging:
            options.set_capability("goog:loggingPrefs", {"browser": "ALL"})

        driver = webdriver.Chrome(
            service=Service(ChromeDriverManager().install()),
            options=options
        )
        driver.maximize_window()
        return driver

    def open(self, url, wait=1):
        print(f"Opening URL: {url}")
        self.driver.get(url)
        time.sleep(wait)

    def get_driver(self):
        return self.driver

    def close(self):
        self.driver.quit()

    def extract_random_numbers_from_console(self):
        logs = self.driver.get_log('browser')
        random_numbers = []

        for log_entry in logs:
            message = log_entry['message']
            lines = message.split("\n")
            for line in lines:
                if "Random number:" in line:
                    try:
                        random_number = int(line.split(": ")[1])
                        random_numbers.append(random_number)
                    except (IndexError, ValueError):
                        continue  # skip malformed lines

        return random_numbers

    def fill_contact_form(self, name, email):
        print("\n\n==== Enter Contact ====\n")
        try:
            element_name = WebDriverWait(self.driver, 0.1).until(
                    EC.presence_of_element_located((By.ID, "name"))
            )
            element_name.send_keys(name)

            element_email = WebDriverWait(self.driver, 0.1).until(
                EC.presence_of_element_located((By.ID, "email"))
            )
            element_email.send_keys(email)
        except Exception as e:
            print(f"Error filling form: {e}")

    def getGameRegion(self):
        
        # Wait for canvas
        wait = WebDriverWait(self.driver, 10)
        canvas = wait.until(EC.presence_of_element_located((By.TAG_NAME, "canvas")))

        # Get canvas position and size (within browser window)
        element_x, element_y = canvas.location['x'], canvas.location['y']
        width, height = canvas.size['width'], canvas.size['height']

        # Get browser window position on screen
        window_position = self.driver.get_window_position()
        browser_x, browser_y = window_position['x'], window_position['y']

        # Adjust for OS window decoration (title bar, etc.)
        # This is platform and browser dependent; here's a general safe margin
        # You may need to calibrate this!
        title_bar_height = 85  # Estimate: try 75–90 for Chrome on Windows
        title_bar_height = 148  # Estimate: try 75–90 for Chrome on Windows
        left_bar_width = 8
        true_x = browser_x + element_x + left_bar_width
        true_y = browser_y + element_y + title_bar_height

        # Region in screen coordinates
        region = (true_x, true_y, width, height)
        return region


