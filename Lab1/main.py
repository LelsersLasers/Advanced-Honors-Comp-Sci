import numpy as np
import argparse
import cv2

#------------------------------------------------------------------------------#
"""
- Image basics: saving loading
- Drawing: rectangle
- Image processing: crop + resize
- Smoothing and blurring: TODO
- Face dectect
- Video

"""

#------------------------------------------------------------------------------#
modelFile = "models/res10_300x300_ssd_iter_140000_fp16.caffemodel"
configFile = "models/deploy.prototxt"
net = cv2.dnn.readNetFromCaffe(configFile, modelFile)

class Face:
    def __init__(self, face):
        self.x = face[0]
        self.y = face[1]
        self.w = face[2]
        self.h = face[3]

        self.center_x = self.x + self.w / 2
        self.center_y = self.y + self.h / 2

    def calc_area(self):
        return self.w * self.h

    def __str__(self):
        return f'Face at {self.center}'
    
    def draw(self, image, color = (255, 0, 0)):
        # rect outline
        cv2.rectangle(image, (self.x, self.y), (self.x+self.w, self.y+self.h), color, 2)
        
def detect_largest_faces(image, conf):
    faces = detect_faces_dnn(image, conf)
    faces.sort(key=Face.calc_area, reverse=True)
    
    if len(faces) < 2:
        raise Exception(f'Not enough faces detected. {len(faces)} detected, at least 2 required.')
    
    return faces
    
def detect_faces_dnn(image, conf):
    blob = cv2.dnn.blobFromImage(image, 1.0, (300, 300), [104, 117, 123], False, False)

    net.setInput(blob)
    detections = net.forward()

    detected_faces = []
    screen_size = (image.shape[1], image.shape[0])

    for i in range(detections.shape[2]):
        confidence = detections[0, 0, i, 2]
        if confidence > conf:
            x1 = int(detections[0, 0, i, 3] * screen_size[0])
            y1 = int(detections[0, 0, i, 4] * screen_size[1])
            x2 = int(detections[0, 0, i, 5] * screen_size[0])
            y2 = int(detections[0, 0, i, 6] * screen_size[1])
            detected_faces.append(Face([x1, y1, x2-x1, y2-y1]))
    
    return detected_faces
#------------------------------------------------------------------------------#


#------------------------------------------------------------------------------#
ap = argparse.ArgumentParser()

ap.add_argument("-i", "--image", required = True, help = "Path to image")
# ap.add_argument("-i", "--input", required = False, help = "Input type (image, video, or camera)")

# ap.add_argument("-v", "--video", required = True, help = "Path to video")

ap.add_argument("-c", "--conf", required = False, help = "Confidence threshold for face detection", default=0.8, type=float)
ap.add_argument("-s", "--save", required = False, help = "Save output to path", default=None)
# TODO: command for face mapping order
args = vars(ap.parse_args())

original_image = cv2.imread(args["image"])
output_image = original_image.copy()

conf = float(args["conf"])
save = args["save"]
#------------------------------------------------------------------------------#


faces = detect_largest_faces(original_image, conf)

for i, face in enumerate(faces):    
    face_crop = original_image[face.y:face.y+face.h, face.x:face.x+face.w]
    next_face = faces[(i+1) % len(faces)]
    face_resized = cv2.resize(face_crop, (next_face.w, next_face.h))
    
    output_image[next_face.y:next_face.y+next_face.h, next_face.x:next_face.x+next_face.w] = face_resized

for face in faces:
    face.draw(original_image)

if save is not None:
    cv2.imwrite(save, output_image)


cv2.imshow("Original", original_image)
cv2.imshow("Output", output_image)

cv2.waitKey(10_000)
    
    