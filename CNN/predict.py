"""
	Description:Use a model to predict the weather from an image or camera.
	Author: Millan Kumar
	Date: 11/29/2023
"""

import argparse

ap = argparse.ArgumentParser()

ap.add_argument(
	"-s",
	"--saved-model-path",
	required=True,
	help="location to load the full model from",
	default=None,
)
ap.add_argument(
	"-i",
	"--input",
	required=True,
	help="input type",
	choices=["image", "camera"],
)
ap.add_argument(
	"-p",
	"--path",
	required=False,
	help="path to image (not required for camera)",
	default=None,
)

args = vars(ap.parse_args())
print(f"\n{args=}\n")

if args["input"] == "image" and args["path"] is None:
	ap.error("image input requires path to image")
# ---------------------------------------------------------------------------- #


# ---------------------------------------------------------------------------- #
import tensorflow as tf
import tensorflow.keras.models as models

classes = ["cloudy", "foggy", "rainy", "shine", "sunrise"]
model = models.load_model(args["saved_model_path"])

print(f"\n\nTensorflow version: {tf.__version__}")
# ---------------------------------------------------------------------------- #


# ---------------------------------------------------------------------------- #
import cv2
import numpy as np

DATA_SHAPE = (387, 387)


def prep_image(image):
	image = cv2.resize(image, DATA_SHAPE)
	image = np.expand_dims(image, axis=0)
	return image

if args["input"] == "image":
	image = cv2.imread(args["path"])
	if image is None:
		ap.error("invalid path to image")

	image = prep_image(image)

	prediction = list(model.predict(image)[0])
	predictions_with_labels = list(zip(prediction, classes))
	predictions_with_labels.sort(reverse=True, key=lambda x: x[0])

	print("\n\nResults:")
	for confidence, label in predictions_with_labels:
		print(f"{label : >8}: {confidence * 100:.2f}%")
else:
	cap = cv2.VideoCapture(0)

	print("Press Q to close")

	while True:
		ret, frame = cap.read()

		if not ret:
			break

		prepped_frame = prep_image(frame)

		prediction = list(model.predict(prepped_frame)[0])
		predictions_with_labels = list(zip(prediction, classes))
		predictions_with_labels.sort(reverse=True, key=lambda x: x[0])

		
		font = cv2.FONT_HERSHEY_SIMPLEX
		bottomLeftCornerOfText = (5, 2)
		fontScale = 0.5
		fontColor = (0, 0, 255)
		thickness = 1
		lineType = 2

		print("\n\nResults:")
		for confidence, label in predictions_with_labels:
			output = f"{label : >8}: {confidence * 100:.2f}%"
			print(output)

			bottomLeftCornerOfText = (bottomLeftCornerOfText[0], bottomLeftCornerOfText[1] + 20)

			cv2.putText(
				frame,
				output,
				bottomLeftCornerOfText,
				font,
				fontScale,
				fontColor,
				thickness,
				lineType,
			)


		cv2.imshow("frame", frame)

		if cv2.waitKey(1) & 0xFF == ord('q'):
			break

	cap.release()
	cv2.destroyAllWindows()