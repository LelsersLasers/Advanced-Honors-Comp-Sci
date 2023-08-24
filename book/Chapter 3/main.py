import argparse
import cv2


ap = argparse.ArgumentParser()
ap.add_argument("-i", "--image", required=True, help="Path to image")

args = vars(ap.parse_args())


image = cv2.imread(args["image"])
print(f"shape: {image.shape[1]} (width), {image.shape[0]} (height) {image.shape[2]} (channels)")
print(f"Whole shape {image.shape}")


cv2.imshow("Image", image)
cv2.waitKey(0)