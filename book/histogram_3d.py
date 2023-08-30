import numpy as np
import argparse
import cv2
from matplotlib import pyplot as plt
import time


ap = argparse.ArgumentParser()
ap.add_argument("-i", "--image", required = True, help = "Path to image")
args = vars(ap.parse_args())


image = cv2.imread(args["image"])
size = 5000
bins = 10

hist = cv2.calcHist([image], [0, 1, 2], None, [bins, bins, bins], [0, 256, 0, 256, 0, 256])
print(f"3d hist shape: {hist.shape}; with {hist.flatten().shape[0]} values")


fig = plt.figure()
ax = fig.add_subplot(111, projection="3d")
ratio = size / np.max(hist)

for (x, plane) in enumerate(hist):
    for (y, row) in enumerate(hist):
        for (z, col) in enumerate(hist):
            if hist[x][y][z] > 0.0:
                siz = ratio * hist[x][y][z]
                rgb = (
                    z / (bins - 1),
                    y / (bins - 1),
                    x / (bins - 1)
                )
                ax.scatter(x, y, z, s = siz, facecolors=rgb)

plt.show()

cv2.waitKey(5000)
