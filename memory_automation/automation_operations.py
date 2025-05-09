# libraries
import time
import os
import random
import pygetwindow

# automation functions
from memory_automation.pair_operations import sortPairs, locatePairs, getPairsArr, getUnmatchedTileNumbers
from memory_automation.screenshot_operations import captureWindow, captureScreenshot, getGameImage
from memory_automation.tile_operations import getUnknownTileSize, findTileInstances, getTilesArr, getTileImages, initializeUnmachtedTiles, clickStart, clickContinue
from memory_automation.browser_operations import Browser


def automateMemoryMatch(Username,Email,MaxLevel):
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

    # Open browser with URL
    browser = Browser(headless=False)
    browser.open(url,6)

    # Get game region
    gameRegion = browser.getGameRegion()
    print(gameRegion)

    getGameImage(gameRegion)

    # set length to 9 for 9 levels 
    current_level = 0
    end_level = MaxLevel

    maxPairs = 6
    numberOfTiles = 12

    # get tiles and pairs arr
    tiles = getTilesArr()
    pairs = getPairsArr()

    # Start total timer
    total_start = time.time()


    while True:

        for level in range(current_level, end_level):

            print("\n\n========== Start Game ==========")

            loop_start = time.time()

            print("Starting with Level: " + str(level))

            clickStart(gameRegion)

            print("\n\n========== Get Logs ==========")

            # Retrieve console logs after start
            random_numbers = browser.extract_random_numbers_from_console()
            print(random_numbers)

            # Check if random_numbers is empty
            if not random_numbers:
                print("No random numbers found in the logs.")
                break  # only valid if this is inside a loop
            else:
                print("Random number: " + str(random_numbers))

            print("\n\n========== New Iteration ==========")
            while len(pairs) < maxPairs:
                # ===== Run Main Funcs ===== #
                # find all unknown tiles
                unmatched_tile_numbers = getUnmatchedTileNumbers(numberOfTiles)

                print("Number of unmatched tiles: " + str(len(unmatched_tile_numbers)) + " Number of pairs: " + str(len(pairs)))
                incremented = [n + 1 for n in unmatched_tile_numbers]
                print("Unmatched Tile numbers: " + str(incremented))

                initializeUnmachtedTiles(gameRegion,unmatched_tile_numbers)

                # get all revealed tile images
                getTileImages()

                # get all pairs
                sortPairs(gameRegion)
 
            # find and locate all pairs
            locatePairs()
            
            # ========================== #
            # delete all tile images
            print("\n\n==== Deleting all Tile Images ====\n")
            for i in range(len(tiles)):
                "./imgRef/tiles/img_" + str(i + 1) + ".png"
                os.remove("./imgRef/tiles/img_" + str(i + 1) + ".png")
            print("Tiles deleted successfully")

            # remove everything in tiles and pairs arr to reset them to be used in next iteration
            print("\n\n==== Clearing arrays ====\n")
            tiles.clear()
            pairs.clear()
            print("Arrays cleared successfully")

            if (level == 0):

                # wait for level complete animation
                time.sleep(6)

                browser.fill_contact_form(Username, Email)

                # Click continue
                clickContinue(gameRegion)

            # wait for level complete animation
            time.sleep(3)

            loop_end = time.time()
            loop_duration = loop_end - loop_start
            print(f"Level {level+1} duration: {loop_duration:.4f} seconds")

        # End total timer
        total_end = time.time()
        total_duration = total_end - total_start
        print(f"Total duration: {total_duration:.4f} seconds")

        user_input = input(
            f"You are at level {level+1}. Enter how many levels to play (or 'q' to quit): "
        )
        if user_input.lower() == 'q':
            print("Exiting program.")
            break
        current_level = level
        levels_to_run = int(user_input)
        end_level = current_level + levels_to_run