import argparse

ap = argparse.ArgumentParser()

ap.add_argument(
	"-l",
	"--load-path",
	required=True,
	help="location to load model from",
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
model = models.load_model(args["load_path"])

print(f"\n\nTensorflow version: {tf.__version__}")
# ---------------------------------------------------------------------------- #


# ---------------------------------------------------------------------------- #
if args["input"] == "image":
	import cv2
	import numpy as np

	image = cv2.imread(args["path"])
	if image is None:
		ap.error("invalid path to image")

	image = cv2.resize(image, (224, 224))

	image = np.expand_dims(image, axis=0)

	prediction = list(model.predict(image)[0])
	predictions_with_labels = list(zip(prediction, classes))

	predictions_with_labels.sort(reverse=True, key=lambda x: x[0])

	print("\n\nResults:")
	for confidence, label in predictions_with_labels:
		print(f"{label : >8}: {confidence * 100:.2f}%")