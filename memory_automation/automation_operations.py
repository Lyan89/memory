# libraries
import time
import os
import random
import pygetwindow

# automation functions
from memory_automation.pair_operations import sortPairs, locatePairs, getPairsArr
from memory_automation.screenshot_operations import captureWindow
from memory_automation.tile_operations import getUnknownTileSize, findTileInstances, getTilesArr, getTileImages, initializeTiles, clickStart
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from webdriver_manager.chrome import ChromeDriverManager

def automateMemoryMatch():
    print("Automation Starting")
    # Load Memory Url from file
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


    # Open url in browser
    driver = webdriver.Chrome(
        service=Service(ChromeDriverManager().install()),
        options=options
    )
    driver.maximize_window()
    driver.get(url)
    time.sleep(1)

    clickStart()

    # Retrieve console logs after your click has been simulated.
    logs = driver.get_log('browser')
    random_numbers = []
    for log_entry in logs:
        message = log_entry['message']
        lines = message.split("\n")
        for line in lines:
            if "Random number:" in line:
                random_number = int(line.split(": ")[1])
                random_numbers.append(random_number)

    print(random_numbers)

    # set length to 9 for 9 levels 
    length = 1
    # get tiles and pairs arr
    tiles = getTilesArr()
    pairs = getPairsArr()



    for i in range(length):
        print("\n\n========== New Iteration ==========")

        # ===== Set up ===== #
        # get current window view and set path
      #  windowPath = captureWindow()
        # find instance of unknown
        #unknownNumber = getUnknownTileSize(windowPath, 0.7)
        # # set unknown path
        # unknownPath = "./imgRef/unknowns/unknown" + unknownNumber + ".png"
        #print("Unknown Path:\t" + unknownPath)

        # ===== Run Main Funcs ===== #
        # find all unknown tiles
        initializeTiles()

        print("Current total tiles: " + str(len(tiles)))

        # get all revealed tile images
        getTileImages()

        # get all pairs
        sortPairs()

        # find and locate all pairs
        locatePairs()
        # ========================== #
        # delete all tile images
        print("\n\n==== Deleting all Tile Images ====\n")
        for i in range(len(tiles)):
            "./imgRef/tiles/img_" + str(i + 1) + ".png"
            os.remove("./imgRef/tiles/img_" + str(i + 1) + ".png")
        print("Tiles deleted successfully")
        # delete the screenshot
     #   os.remove("./imgRef/misc/currentBoard.png")
      #  print("Screenshot deleted")

        # remove everything in tiles and pairs arr to reset them to be used in next iteration
        print("\n\n==== Clearing arrays ====\n")
        tiles.clear()
        pairs.clear()
        print("Arrays cleared successfully")

        # wait for level complete animation
        time.sleep(3)

