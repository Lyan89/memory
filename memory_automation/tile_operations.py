# libraries
import cv2 as cv
import numpy as np
import pyautogui
import time
import os

# automation functions
from memory_automation.screenshot_operations import captureScreenshot


# declare tile class to create instances and add to arr of tiles
class Tile:
    def __init__(self, tileName,tileNumber , x, y, w, h, centerX, centerY):
        self.tileName = tileName
        self.tileNumber = tileNumber
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.centerX = centerX
        self.centerY = centerY
tiles = []

def clickStart(gameRegion):

    scale = gameRegion[2]/705 # Scaling in case game region is different than originally currentWidth/designerwidth

    offsetx = int(0*scale)
    offsety = int(805*scale)

    clickx = int(gameRegion[0] + gameRegion[2]/2+offsetx)
    clicky = int(gameRegion[1] + offsety)

    print(clickx)
    print(clicky)
    pyautogui.moveTo(clickx, clicky)   # moves mouse
    pyautogui.click()  # click the mouse
    time.sleep(1)

def clickContinue(gameRegion):

    scale = gameRegion[2]/705 # Scaling in case game region is different than originally currentWidth/designerwidth

    offsetx = int(0*scale) 
    offsety = int(815*scale)

    clickx = int(gameRegion[0] + gameRegion[2]/2+offsetx)
    clicky = int(gameRegion[1] + offsety)

    
    pyautogui.moveTo(clickx, clicky)   # moves mouse
    pyautogui.click()  # click the mouse
    time.sleep(1)

# get tiles arr
def getTilesArr():
    return tiles

def initializeUnmachtedTiles(gameRegion,unmatched_tile_numbers):

    tiles.clear()

    region = gameRegion

    scale = gameRegion[2]/705 # Scaling in case game region is different than originally currentWidth/designerwidth

    clickdistancex = int(220*scale) # x-distance between click tiles
    clickdistancey = int(250*scale) # y-distance between click tiles

    clickoffsetx = int(1*scale) # Offset between canvas top and first tile center
    clickoffsety = int(263*scale) # Offset between canvas top and first tile center

    startclickx = int(region[0] + region[2]/2 - clickdistancex + clickoffsetx)
    startclicky = int(region[1] + clickoffsety)

    # print("startclickx: " + str(startclickx) + " startclicky: " + str(startclicky))


    tiledistancex = int(261*scale) # x-distance between tiles
    tiledistancey = int(298*scale) # y-distance between tiles

    tileoffsetx = int(-113*scale) # Offset between canvas top and first tile center
    tileoffsety = int(83*scale) # Offset between canvas top and first tile center

    starttilex = int(region[0] + region[2]/2 - tiledistancex + tileoffsetx)
    starttiley = int(region[1] + tileoffsety)

    # print("starttilex: " + str(starttilex) + " starttiley: " + str(starttiley))

    cropclearance = int(22*scale) # images need be cropped by this much (Since not full size is visible everywhere)

    cropclearance = 0 # images need be cropped by this much (Since not full size is visible everywhere)

    tilewidth = int(228*scale) # Width of the tiles
    tileheight = int(228*scale) # Height of the tiles

    rows = 3
    columns = 4
    counter = 0
    for column in range(columns):
        for row in range(rows):
        
            
            centerX = startclickx + row*clickdistancex
            centerY = startclicky + column*clickdistancey

            x = starttilex + row*tiledistancex + cropclearance
            y = starttiley + column*tiledistancey + cropclearance

            w = tilewidth -2*cropclearance
            h = tileheight -2*cropclearance

            # add rect data to tiles arr if unmachted
            if counter in unmatched_tile_numbers:
                tiles.append(Tile("tile_" + str(counter),counter , x, y, w, h, centerX, centerY))
            counter = counter + 1



# find all instances of unknown tiles
def findTileInstances(baseImagePath, isolatedImagePath, thresholdVal, mode, lineColor = (0, 0, 255)):
    # display title in console for this func running
    print("\n\n==== Finding All Unknowns ====\n")

    # define imgs as variables 
    baseImage = cv.imread(baseImagePath, cv.IMREAD_COLOR)
    isolatedImage = cv.imread(isolatedImagePath, cv.IMREAD_COLOR)

    # check img properties
    # print(
    #     "img1 shape\t" + str(baseImage.shape[1]) + "\n"
    #     "img1 shape\t" + str(baseImage.shape[0]) + "\n"
    #     "img2 shape\t" + str(isolatedImage.shape[1]) + "\n"
    #     "img2 shape\t" + str(isolatedImage.shape[0]) + "\n"
    #     "img1 type\t" + str(baseImage.dtype) + "\n"
    #     "img2 type\t" + str(isolatedImage.dtype) + "\n"
    #     "img1 idk\t" + str(baseImage.ndim) + "\n"
    #     "img2 idk\t" + str(isolatedImage.ndim) + "\n"
    # )

    # save dimenshions of img
    isolatedImageW = isolatedImage.shape[1]
    isolatedImageH = isolatedImage.shape[0]

    # set a threshold for matching accuracy
    threshold = thresholdVal

    # match isolatedImage against baseImage with 1 of the following methods
    # TM_CCOEFF, TM_CCOEFF_NORMED, TM_CCORR, TM_CCORR_NORMED, TM_SQDIFF, TM_SQDIFF_NORMED
    method = cv.TM_CCOEFF_NORMED
    result = cv.matchTemplate(baseImage, isolatedImage, method)
    
    # Get all positions from the match result that exceed the threshold (retunrs array)
    locations = np.where(result >= threshold)
    # refine the locations array to just return x and y coordinates of each matched location
    locations = list(zip(*locations[::-1]))

    # create list of rectangles [x, y, w, h] (so they can be grouped together) 
    rectangles = []
    for l in locations:
        rect = [int(l[0]), int(l[1]), isolatedImageW, isolatedImageH]
        # Add every box to the list twice in order to retain single (non-overlapping) boxes
        rectangles.append(rect)
        rectangles.append(rect)

    # group rectangles that are close to each other where 3rd parameter controls how close together they must be to be grouped
    rectangles, weights = cv.groupRectangles(rectangles, 1, 0.5)

    points = []
    if len(rectangles):
        # set counter to 1 for naming convention
        counter = 1
        # set rect properties
        lineColor = lineColor # (B,G,R)
        lineThickness = 2
        lineType = cv.LINE_8
        markerColor = lineColor # (B,G,R)
        markerType = cv.MARKER_CROSS
        markerSize = 30
        markerThickness = 2

        # loop over each location
        for (x, y, w, h) in rectangles:
            # determine rect pos
            topLeft = (x, y)
            bottomRight = (x + w, y + h)
            # get center of rect
            centerX = x + int(w/2)
            centerY = y + int(h/2)
            # add rect data to tiles arr
            tiles.append(Tile("tile_" + str(counter), x, y, w, h, centerX, centerY))

            if mode == "rectangles":
                # draw the rect
                cv.rectangle(baseImage, topLeft, bottomRight, lineColor, lineThickness, lineType)

            elif mode == "points":
                # save points
                points.append((centerX, centerY))
                # draw the center point
                cv.drawMarker(baseImage, (centerX, centerY), markerColor, markerType, markerSize, markerThickness)
            # increment counter
            counter += 1

        if mode:
            # display baseImage with matched data
            # cv.imshow("Matched Image", baseImage)
            # cv.waitKey()
            print("All Unknowns identified")
            # save the image
            # cv.imwrite('result_click_point.jpg', haystack_img)

    else:
        print("Didn't find any matches")



# get unknown size
def getUnknownTileSize(baseImagePath, thresholdVal):
    # display title in console for this func running
    print("\n\n==== Finding Unknown Size ====\n")

    # amount of unknown tile sizes
    length = 10

    # loop through all unknown images
    for i in range(length):
        # define imgs as variables 
        baseImage = cv.imread(baseImagePath, cv.IMREAD_COLOR)
        isolatedImage = cv.imread("./imgRef/unknowns/unknown" + str(i + 1) + ".png", cv.IMREAD_COLOR)

        # match isolatedImage against baseImage with 1 of the following methods
        # TM_CCOEFF, TM_CCOEFF_NORMED, TM_CCORR, TM_CCORR_NORMED, TM_SQDIFF, TM_SQDIFF_NORMED
        method = cv.TM_CCOEFF_NORMED
        result = cv.matchTemplate(baseImage, isolatedImage, method)
        
        # Get all positions from the match result that exceed the threshold (retunrs array)
        locations = np.where(result >= thresholdVal)
        # refine the locations array to just return x and y coordinates of each matched location
        locations = list(zip(*locations[::-1]))
        
        currentUnknownPath = ""
        # when there is a match, return unknown path
        if len(locations) != 0:
            # set match as the board path
            currentUnknownPath = str(i + 1)
            print("Unknown " + str(i + 1))
            return currentUnknownPath
        
        else:
            currentUnknownPath = "\t No unknowns found"

    print(currentUnknownPath)
    return currentUnknownPath



# reveal unknowns and take imgs
def getTileImages():
    # new section of data display
    print("\n\n==== Getting Tile Images ====\n")
    
    # check for (and create if missing) tiles subdir
    tilesPath = os.path.exists("./imgRef/tiles")
    if not tilesPath:
        os.makedirs("./imgRef/tiles")
        print("made missing tiles directory")
        
    counter = 1
    length = len(tiles)
    # iterate over each tile in tiles arr

    for i in range(length):
        print(
            "tile name: " + tiles[i].tileName,
            "\n\tx coord: " + str(tiles[i].x), 
            "\n\ty coord: " + str(tiles[i].y), 
            "\n\twidth val: " + str(tiles[i].w), 
            "\n\theight val: " + str(tiles[i].h), 
            "\n\tcenter x coord: " + str(tiles[i].centerX), 
            "\n\tcenter y coord: " + str(tiles[i].centerY),
            "\n----\n"
        )
        # move cursor to tile
        pyautogui.moveTo(tiles[i].centerX, tiles[i].centerY)
        # click tile to reveal image
        pyautogui.click()
        time.sleep(0.5)
        # take image at given coords
        captureScreenshot("./tiles/img_" + str(counter) + ".png", "coords", tiles[i].x, tiles[i].y, tiles[i].w, tiles[i].h)
        counter += 1
        time.sleep(0.5)
    
    print("revealed all tile imgs")


