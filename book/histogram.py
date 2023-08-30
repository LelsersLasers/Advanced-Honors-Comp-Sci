import numpy as np
import argparse
import cv2
from matplotlib import pyplot as plt


ap = argparse.ArgumentParser()
ap.add_argument("-i", "--image", required = True, help = "Path to image")
args = vars(ap.parse_args())


image = cv2.imread(args["image"])

gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
cv2.imshow("Ori gray", gray)


hist = cv2.calcHist([gray], [0], None, [256], [0, 256])

plt.figure()
plt.title("Grayscale Histogram")
plt.xlabel("Bin")
plt.ylabel("# of pixels")
plt.plot(hist)
plt.xlim([0, 256])
plt.show()

# cv2.waitKey(5000)

chans = cv2.split(image)
colors = ("b", "g", "r")
plt.figure()
plt.title("'Flattened' Color Histogram")
plt.xlabel("Bin")
plt.ylabel("# of pixels")

for (chan, color) in zip(chans, colors):
    hist = cv2.calcHist([chan], [0], None, [256], [0, 256])
    plt.plot(hist)
    plt.xlim([0, 256])
plt.show()

cv2.waitKey(5000)
