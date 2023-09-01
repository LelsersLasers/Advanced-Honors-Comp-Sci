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
blurred = cv2.GaussianBlur(gray, (5, 5), 0)
# blurred = cv2.bilateralFilter(gray, 7, 41, 41),

cv2.imshow("Image", blurred)

# Canny
canny = cv2.Canny(blurred, 30, 150)
cv2.imshow("Canny", canny)

cv2.waitKey(10000)
