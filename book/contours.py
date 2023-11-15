import numpy as np
import argparse
import imutils
import mahotas # for Otsu and Riddler-Calvard
import cv2


ap = argparse.ArgumentParser()
ap.add_argument("-i", "--image", required = True, help = "Path to image")
args = vars(ap.parse_args())


image = cv2.imread(args["image"])
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
blurred = cv2.GaussianBlur(gray, (11, 11), 0)
# blurred = cv2.bilateralFilter(gray, 7, 41, 41),

# cv2.imshow("Image", blurred)

edged = cv2.Canny(blurred, 30, 150)
# cv2.imshow("Edges", edged)

(cnts, _) = cv2.findContours(edged.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

print("# of countors", len(cnts))

coins = image.copy()
cv2.drawContours(coins, cnts, -1, (0, 255, 0), -1)
# cv2.drawContours(coins, cnts, -1, (0, 255, 255), 20)
# cv2.imshow("Coins", coins)

# cv2.waitKey(10000)
cv2.imwrite("test.png", coins)

