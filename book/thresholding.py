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

cv2.imshow("Image", image)


# Manual
(T, thresh) = cv2.threshold(blurred, 155, 255, cv2.THRESH_BINARY)
cv2.imshow("Thresh binary", thresh)

merged = cv2.bitwise_and(image, image, mask = thresh)
cv2.imshow("Merge", merged)

# Adaptive
thresh_adaptive_mean = cv2.adaptiveThreshold(blurred, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY_INV, 11, 4)
cv2.imshow("Mean thresh", cv2.bitwise_and(image, image, mask = thresh_adaptive_mean))

thresh_adaptive_guassain = cv2.adaptiveThreshold(blurred, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV, 15, 3)
cv2.imshow("Guassian thresh", cv2.bitwise_and(image, image, mask = thresh_adaptive_guassain))

# Otsu
T = mahotas.thresholding.otsu(blurred)
print(f"Otsu's threshhold {T}")

thresh = gray.copy()
thresh[thresh > T] = 255
thresh[thresh < 255] = 0
thresh = cv2.bitwise_not(thresh)
cv2.imshow("Otsu", thresh)

# Riddler-Calvard
T = mahotas.thresholding.rc(blurred)
print(f"Riddler-Calvard's threshhold {T}")

thresh = gray.copy()
thresh[thresh > T] = 255
thresh[thresh < 255] = 0
thresh = cv2.bitwise_not(thresh)
cv2.imshow("Riddler-Calvard", thresh)

cv2.waitKey(5000)
