# Convert all images in folder to png format

import os
import cv2

dataset_folder = "dataset2"

for folder in os.listdir(dataset_folder):
	for filename in os.listdir(dataset_folder + '/' + folder):
		print(dataset_folder + '/' + folder + '/' + filename)

		if filename.endswith('.png'):
			continue

		if not filename.endswith('.gif'):
			image = cv2.imread(dataset_folder + '/' + folder + '/' + filename)
			cv2.imwrite(dataset_folder + '/' + folder + '/' + filename.split('.')[0] + '.png', image)

		# delete old file
		os.remove(dataset_folder + '/' + folder + '/' + filename)