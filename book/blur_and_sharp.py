import numpy as np
import argparse
import imutils
import cv2


ap = argparse.ArgumentParser()
ap.add_argument("-i", "--image", required = True, help = "Path to image")
args = vars(ap.parse_args())


image = cv2.imread(args["image"])

blurred = np.hstack([
    cv2.blur(image, (3, 3)),
    cv2.blur(image, (5, 5)),
    cv2.blur(image, (7, 7))
])
cv2.imshow("Averaged", blurred)


# 0 => auto compute standard deviation in x-axis direction
blurred_gaussian = np.hstack([
    cv2.GaussianBlur(image, (3, 3), 0),
    cv2.GaussianBlur(image, (5, 5), 0),
    cv2.GaussianBlur(image, (7, 7), 0),
])
cv2.imshow("Guassian", blurred_gaussian)

blurred_median = np.hstack([
    cv2.medianBlur(image, 3),
    cv2.medianBlur(image, 5),
    cv2.medianBlur(image, 7),
])
cv2.imshow("Median", blurred_median)

blurred_bilateral = np.hstack([
    cv2.bilateralFilter(image, 3, 21, 21),
    cv2.bilateralFilter(image, 5, 31, 31),
    cv2.bilateralFilter(image, 7, 41, 41),
])
cv2.imshow("Bilteral", blurred_bilateral)


cv2.waitKey(10000)