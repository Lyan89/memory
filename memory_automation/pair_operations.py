# libraries
import cv2 as cv
import numpy as np
import pyautogui
import time

# automation functions
from memory_automation.tile_operations import getTilesArr


# declare pair class for matching pairs
class Pair:
    def __init__(self, pairName, t1, t2, tile1_num, tile2_num,uncovered):
        self.pairName = pairName
        self.t1 = t1
        self.t2 = t2
        self.tile1_num = tile1_num  # tile index or number
        self.tile2_num = tile2_num
        self.uncovered = uncovered
pairs = []



# get pairs arr
def getPairsArr():
    return pairs


def cropImage(image, frameSize):
    # Remove frameSize pixels from each side
    cropped_image = image[frameSize:-frameSize, frameSize:-frameSize]
    return cropped_image


# check if 2 imgs match
def matchPair(imgPath1, imgPath2, thresholdVal,frameSize):
    # define imgs as variables 
    img1 = cropImage(cv.imread(imgPath1, cv.IMREAD_UNCHANGED),frameSize)
    img2 = cropImage(cv.imread(imgPath2, cv.IMREAD_UNCHANGED),frameSize)

    # check dimensions
    # print(
    #     img1.shape[0],
    #     img1.shape[1],
    #     img2.shape[0],
    #     img2.shape[1],
    # )

    # set a threshold for matching accuracy
    threshold = thresholdVal

    # match img2 against img1 with 1 of the following methods
    # TM_CCOEFF, TM_CCOEFF_NORMED, TM_CCORR, TM_CCORR_NORMED, TM_SQDIFF, TM_SQDIFF_NORMED
    method = cv.TM_CCOEFF_NORMED
    result = cv.matchTemplate(img1, img2, method)
    
    # Get all positions from the match result that exceed the threshold (retunrs array)
    locations = np.where(result >= threshold)
    # refine the locations array to just return x and y coordinates of each matched location
    locations = list(zip(*locations[::-1]))

    # return true or false depending on if images matched
    if len(locations) >= 1:
        # print("p")
        return True
    else:
        # print("n")
        return False
    


def sortPairs(gameRegion):
    scale = gameRegion[2] / 705
    frameSize = int(22 * scale)

    tiles = getTilesArr()
    print("\n\n==== Getting All Tile Pairs ====\n")

    pairCount = len(pairs)  # Assuming 'pairs' is a global list
    matched = set()
    length = len(tiles)

    for i in range(length):
        if i in matched:
            continue

        for j in range(i + 1, length):
            if j in matched:
                continue

            match = matchPair(
                f"./imgRef/tiles/img_{i + 1}.png",
                f"./imgRef/tiles/img_{j + 1}.png",
                thresholdVal=0.8,
                frameSize=frameSize
            )

            if match:
                pairCount += 1
                matched.update([i, j])

                uncovered = ((j - i) == 1) and ((j % 2) != 0) and ((tiles[j].tileNumber - tiles[i].tileNumber) == 1)

                print(f"Pair {pairCount}{' (uncovered)' if uncovered else ''}: {i + 1} and {j + 1}")

                pairs.append(Pair(
                    f"Pair_{pairCount}",
                    [tiles[i].centerX, tiles[i].centerY],
                    [tiles[j].centerX, tiles[j].centerY],
                    i,
                    j,
                    uncovered
                ))
                break  # Once tile i is matched, go to next i

    # 🔒 Failsafe: if exactly 2 unmatched tiles remain, force pair them
    unmatched = [idx for idx in range(length) if idx not in matched]
    if len(unmatched) == 2:
        i, j = unmatched
        pairCount += 1
        print(f"Failsafe Pair {pairCount}: {i + 1} and {j + 1} (forced match)")

        pairs.append(Pair(
            f"Pair_{pairCount}",
            [tiles[i].centerX, tiles[i].centerY],
            [tiles[j].centerX, tiles[j].centerY],
            i,
            j,
            uncovered=False
        ))
        matched.update(unmatched)



def getUnmatchedTileNumbers(expectedNumberOfTiles):
    # All expected tile numbers from 0 to expectedNumberOfTiles - 1

    all_tile_numbers = set(range(expectedNumberOfTiles))
    
    # Tile numbers found in pairs
    paired_tile_numbers = set()
    for pair in pairs:
        paired_tile_numbers.add(pair.tile1_num)
        paired_tile_numbers.add(pair.tile2_num)
        
    # Unmatched tile numbers = all - those in pairs
    unmatched_tile_numbers = list(all_tile_numbers - paired_tile_numbers)
    
    return sorted(unmatched_tile_numbers)

import time
import pyautogui

def locatePairs():
    time.sleep(0.5)
    print("\n\n==== Locating All Pairs ====\n")

    # Sort pairs by the highest tile number of either tile1_num or tile2_num, in descending order
    sorted_pairs = sorted(pairs, key=lambda p: max(p.tile1_num, p.tile2_num), reverse=True)

    for pair in sorted_pairs:
         # print(
         #     pair.pairName,
         #     "\nPosition 1 - \n\t" + "x: " + str(pair.t1[0]) + "\n\ty: " + str(pair.t1[1]), 
         #     "\nPosition 2 - \n\t" + "x: " + str(pair.t2[0]) + "\n\ty: " + str(pair.t2[1]),
         #     "\n-------------"
         # )
        # Skip if already uncovered
        if pair.uncovered == False:
            pyautogui.moveTo(pair.t1[0], pair.t1[1])
            pyautogui.click()
            time.sleep(0.5)

            pyautogui.moveTo(pair.t2[0], pair.t2[1])
            pyautogui.click()
            time.sleep(0.5)

    print("All pairs located successfully")


