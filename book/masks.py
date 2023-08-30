
import numpy as np
import argparse
import cv2


ap = argparse.ArgumentParser()
ap.add_argument("-i", "--image", required = True, help = "Path to image")
args = vars(ap.parse_args())


image = cv2.imread(args["image"])
cv2.imshow("Ori", image)

mask = np.zeros(image.shape[:2], dtype="uint8")
c_x = image.shape[1] // 2
c_y = image.shape[0] // 2
cv2.rectangle(mask, (c_x - 75, c_y - 75), (c_x + 75, c_y + 75), 255, -1)
cv2.imshow("Mask", mask)

masked = cv2.bitwise_and(image, image, mask = mask)
cv2.imshow("Masked", masked)

cv2.waitKey(5000)