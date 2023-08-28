import numpy as np
import argparse
import imutils
import cv2


ap = argparse.ArgumentParser()
ap.add_argument("-i", "--image", required = True, help = "Path to image")
args = vars(ap.parse_args())


image = cv2.imread(args["image"])
cv2.imshow("Ori", image)

cv2.imshow("Updated", imutils.flip(image))
cv2.waitKey(5000)