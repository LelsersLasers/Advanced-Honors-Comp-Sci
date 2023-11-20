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
    choices=["image", "video", "camera"],
)
ap.add_argument(
    "-p",
    "--path",
    required=False,
    help="path to image or video (not required for camera)",
    default=None,
)
ap.add_argument(
    "-c",
    "--confidence",
    required=False,
    help="confidence threshold for face detection",
    default=0.8,
    type=float,
)
ap.add_argument(
    "-w",
    "--wait-time",
    required=False,
    help="how long to wait before removing a face (only for `-i video)`",
    default=0.2,
    type=float,
)

args = vars(ap.parse_args())
print(f"\n{args=}\n")

if args["input"] == "image" and args["path"] is None:
	ap.error("image input requires path to image")
# ---------------------------------------------------------------------------- #


# ---------------------------------------------------------------------------- #
import tensorflow as tf
import tensorflow.keras.models as models

classes = ["Angry", "Happy", "Sad"]
model = models.load_model(args["load_path"])

print(f"\n\nTensorflow version: {tf.__version__}")
# ---------------------------------------------------------------------------- #


# ---------------------------------------------------------------------------- #
import cv2
import time
import numpy as np
import face_detect


def prep_image(image):
	image = cv2.resize(image, (224, 224))
	image = np.expand_dims(image, axis=0)
	return image

def write_text(image, text, bottomLeftCornerOfText):
	font = cv2.FONT_HERSHEY_SIMPLEX
	fontScale = 0.5
	fontColor = (0, 0, 255)
	thickness = 1
	lineType = 2

	cv2.putText(
		image,
		text,
		bottomLeftCornerOfText,
		font,
		fontScale,
		fontColor,
		thickness,
		lineType,
	)

def predict(image, face_detection):
	crop = image[face_detection.y:face_detection.y2, face_detection.x:face_detection.x2]
	if crop.shape[0] < 10 or crop.shape[1] < 10:
		return

	crop = prep_image(crop)
	
	prediction = list(model.predict(crop)[0])
	predictions_with_labels = list(zip(prediction, classes))
	predictions_with_labels.sort(reverse=True, key=lambda x: x[0])
	output = f"{predictions_with_labels[0][1]}: {predictions_with_labels[0][0] * 100:.2f}%"

	write_text(image, output, (face_detection.x - 3, face_detection.y - 3))


if args["input"] == "image":
	image = cv2.imread(args["path"])
	if image is None:
		ap.error("invalid path to image")

	face_detections = face_detect.detect_faces(image, args["confidence"])

	for face_detection in face_detections:
		predict(image, face_detection)
		face_detection.draw_debug(image)

	cv2.imshow("Output", image)
	cv2.waitKey(0)
else:
	cap = cv2.VideoCapture(0)

	print("Press Q to close")

	t0 = time.time()
	t1 = time.time()
	delta = 1 / 15

	face_orderings = []

	while True:
		ret, frame = cap.read()
		if not ret:
			break

		t1 = time.time()
		delta = t1 - t0
		t0 = t1

		face_detect.detect_faces_and_update_ordering(frame, args["confidence"], face_orderings, args["wait_time"], delta)

		for face_ordering_data in face_orderings:
			predict(frame, face_ordering_data.face)
			face_ordering_data.draw_debug(frame, args["wait_time"])


		cv2.imshow("Output", frame)

		if cv2.waitKey(1) & 0xFF == ord('q'):
			break

	cap.release()
	cv2.destroyAllWindows()