canvaspositionx = 927
canvaspositiony = 140
canvaswidth = 689
canvasheight = 1225
offsetx = 220
offsety = 250

tilewidth = 206 #192
tileheight = 229 #192
startoffsety = 263 # Offset from canvas top to first tile click

tileimageoffsetx = 21
tileimageoffsety = 63
rows = 3
columns = 4

startclickx = int(canvaspositionx + canvaswidth/2 - offsetx)
startclicky = int(canvaspositiony + startoffsety)

print("startclickx: " + str(startclickx) + "startclicky: " + str(startclicky))
counter = 0
for row in range(rows):
    for column in range(columns):
        counter = counter + 1
        centerX = startclickx + row*offsetx
        centerY = startclicky + column*offsety

        print("Centerx: " + str(centerX) + "Centery: " + str(centerY))
        x = int(centerX-tilewidth/2-tileimageoffsetx)
        y = int(centerY-tileheight/2-tileimageoffsety)

        print("x: " + str(x) + "y: " + str(y))
        #w = tilewidth
        #h = tileheight