import numpy as np
import argparse
import cv2
from matplotlib import pyplot as plt
import time


ap = argparse.ArgumentParser()
ap.add_argument("-i", "--image", required = True, help = "Path to image")
args = vars(ap.parse_args())


image = cv2.imread(args["image"])


chans = cv2.split(image)

# fig = plt.figure()

# ax = fig.add_subplot(131)
# hist = cv2.calcHist([chans[1], chans[0]], [0, 1], None, [32, 32], [0, 256, 0, 256])
# p = ax.imshow(hist, interpolation = "nearest")
# ax.set_title("2d Color histogram for G and B")
# plt.colorbar(p)

# ax = fig.add_subplot(132)
# hist = cv2.calcHist([chans[1], chans[2]], [0, 1], None, [32, 32], [0, 256, 0, 256])
# p = ax.imshow(hist, interpolation = "nearest")
# ax.set_title("2d Color histogram for G and R")
# plt.colorbar(p)

# ax = fig.add_subplot(133)
# hist = cv2.calcHist([chans[0], chans[2]], [0, 1], None, [32, 32], [0, 256, 0, 256])
# p = ax.imshow(hist, interpolation = "nearest")
# ax.set_title("2d Color histogram for B and R")
# plt.colorbar(p)

fig = plt.figure()
ax = fig.add_subplot(131)
hist = cv2.calcHist([chans[1], chans[0]], [0, 1], None, [32, 32], [0, 256, 0, 256])
p = ax.imshow(hist, interpolation = "nearest")
ax.set_title("2D Color Histogram for G and B")
plt.colorbar(p)
ax = fig.add_subplot(132)
hist = cv2.calcHist([chans[1], chans[2]], [0, 1], None, [32, 32], [0, 256, 0, 256])
p = ax.imshow(hist, interpolation = "nearest")
ax.set_title("2D Color Histogram for G and R")
plt.colorbar(p)
ax = fig.add_subplot(133)
hist = cv2.calcHist([chans[0], chans[2]], [0, 1], None, [32, 32], [0, 256, 0, 256])
p = ax.imshow(hist, interpolation = "nearest")
ax.set_title("2D Color Histogram for B and R")
plt.colorbar(p)

plt.show()

cv2.waitKey(5000)
