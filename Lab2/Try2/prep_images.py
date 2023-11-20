# Convert all images in folder to png format

import os
import cv2
import face_detect

dataset_folder = "dataset"
datasetModified_folder = "datasetModified"

i = 0

for folder in os.listdir(dataset_folder):
	for filename in os.listdir(dataset_folder + '/' + folder):
		print(dataset_folder + '/' + folder + '/' + filename)

		if filename.endswith('.gif'):
			continue
		

		image = cv2.imread(dataset_folder + '/' + folder + '/' + filename)
		face_detections = face_detect.detect_faces(image, 0.75)

		for face_detection in face_detections:
			crop = image[face_detection.y:face_detection.y2, face_detection.x:face_detection.x2]
			if crop.shape[0] < 30 or crop.shape[1] < 30:
				continue
			image = cv2.resize(crop, (224, 224))
			cv2.imwrite(datasetModified_folder + '/' + folder + '/' + str(i) + '.png', image)
			i += 1