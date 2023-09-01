import numpy as np
from matplotlib import pyplot as plt
import argparse
import cv2


ap = argparse.ArgumentParser()
ap.add_argument("-i", "--image", required = True, help = "Path to image")
args = vars(ap.parse_args())

def plot_histogram(image, title, mask = None):
    chans = cv2.split(image)
    colors = ("b", "g", "r")
    plt.figure()
    plt.title(title)
    plt.xlabel("Bins")
    plt.ylabel("# of Pixels")

    for (chan, color) in zip(chans, colors):
        hist = cv2.calcHist([chan], [0], mask, [256], [0, 256])
        plt.plot(hist, color = color)
        plt.xlim([0, 256])


image = cv2.imread(args["image"])
plot_histogram(image, "Hist Ori")


mask = np.zeros(image.shape[:2], dtype = "uint8")
cv2.rectangle(mask, (15, 15), (130, 100), 255, -1)
cv2.imshow("Mask", mask)

masked = cv2.bitwise_and(image, image, mask = mask)
cv2.imshow("Masked", masked)

plot_histogram(image, "Hist Masked", mask = mask)

plt.show()

# gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

# eq = cv2.equalizeHist(gray)

# cv2.imshow("Histogram Equalization", np.hstack([gray, eq]))
cv2.waitKey(10000)