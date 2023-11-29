"""
    Description: Functions and classes for detecting and managing faces
    Author: Millan and Jerry
    Date: 9/27/2023
"""

import cv2

config_file = "face_models/deploy.prototxt"
model_file = "face_models/res10_300x300_ssd_iter_140000_fp16.caffemodel"
net = cv2.dnn.readNetFromCaffe(config_file, model_file)


class DetectedFace:
    """Dimensions for a detected face"""

    def __init__(self, x, y, w, h):
        self.x = x
        self.y = y
        self.w = w
        self.h = h

        self.x2 = x + w # Bottom right x
        self.y2 = y + h # Bottom right y

        self.center_x = x + w / 2
        self.center_y = y + h / 2

    def __str__(self):
        return f"Detected Face with center: ({self.center_x}, {self.center_y})"
    
    def __repr__(self):
        return f"DetectedFace({self.x}, {self.y}, {self.w}, {self.h})"

    def get_center_tuple(self):
        return (self.center_x, self.center_y)
    
    def get_center_tuple_int(self):
        return (int(self.center_x), int(self.center_y))
    
    def draw_debug(self, output_image):
        cv2.rectangle(output_image, (self.x, self.y), (self.x2, self.y2), (255, 0, 0), 2)

class FaceOrderingData:
    """Data for a face that is being tracked between frames"""

    def __init__(self, face):
        self.face = face
        self.last_center = face.get_center_tuple()
        self.time_since_seen = 0.0

    def draw_debug(self, output_image, wait_time):
        self.face.draw_debug(output_image)
        if self.time_since_seen > 0:
            # white->black = seen recently->not seen recently
            ratio = self.time_since_seen / wait_time
            color_intensity = int(255 * (1 - ratio))
            color = (color_intensity, color_intensity, color_intensity)
            cv2.circle(output_image, self.face.get_center_tuple_int(), 5, color, -1)

def dist_between(p1, p2):
    """Returns the distance between two points"""
    return ((p1[0] - p2[0])**2 + (p1[1] - p2[1])**2)**0.5

def detect_faces(image, confidence_threshold, use_whole = False):
    """Uses a deep neural network to detect faces in an image and returns a list of DetectedFaces"""

    blob = cv2.dnn.blobFromImage(image, 1.0, (300, 300), [104, 117, 123], False, False)

    net.setInput(blob)
    detections = net.forward()

    detected_faces = []
    screen_size = (image.shape[1], image.shape[0])

    for i in range(detections.shape[2]):
        confidence = detections[0, 0, i, 2]
        if confidence > confidence_threshold:
            x1 = int(detections[0, 0, i, 3] * screen_size[0])
            y1 = int(detections[0, 0, i, 4] * screen_size[1])
            x2 = int(detections[0, 0, i, 5] * screen_size[0])
            y2 = int(detections[0, 0, i, 6] * screen_size[1])

            w = x2 - x1
            h = y2 - y1

            detected_face = DetectedFace(x1, y1, w, h)
            detected_faces.append(detected_face)

    if use_whole:
        detected_faces.append(DetectedFace(0, 0, image.shape[1], image.shape[0]))

    return detected_faces

def detect_faces_and_update_ordering(image, confidence_threshold, face_orderings, wait_time, delta):
    """Detects faces in an image and updates the ordering list"""

    detected_faces = detect_faces(image, confidence_threshold)

    used_detected_faces_idxs = []
    used_face_orderings_idxs = []

    while len(used_detected_faces_idxs) < min(len(detected_faces), len(face_orderings)):
        closest_detected_face_idx = None
        closest_face_orderings_idx = None
        closest_dist = float("inf")

        for face_ordering_idx, face_orderings_face in enumerate(face_orderings):
            if face_ordering_idx in used_face_orderings_idxs:
                continue

            for detected_face_idx, detected_face in enumerate(detected_faces):
                if detected_face_idx in used_detected_faces_idxs:
                    continue

                dist = dist_between(face_orderings_face.last_center, detected_face.get_center_tuple())
                if dist < closest_dist:
                    closest_detected_face_idx = detected_face_idx
                    closest_face_orderings_idx = face_ordering_idx
                    closest_dist = dist

        used_detected_faces_idxs.append(closest_detected_face_idx)
        used_face_orderings_idxs.append(closest_face_orderings_idx)

        closest_detected_face = detected_faces[closest_detected_face_idx]
        face_orderings[closest_face_orderings_idx] = FaceOrderingData(closest_detected_face)

    if len(detected_faces) > len(face_orderings):
        for detected_face_idx, detected_face in enumerate(detected_faces):
            if detected_face_idx in used_detected_faces_idxs:
                continue
            
            face_ordering_data = FaceOrderingData(detected_face)
            face_orderings.append(face_ordering_data)
    elif len(detected_faces) < len(face_orderings):
        face_orderings_idxs_to_update = []

        for face_ordering_idx in range(len(face_orderings)):
            if face_ordering_idx not in used_face_orderings_idxs:
                face_orderings_idxs_to_update.append(face_ordering_idx)

        # reverse order so we can delete in iteration
        for face_ordering_idx in reversed(face_orderings_idxs_to_update):
            face_ordering_data = face_orderings[face_ordering_idx]
            if face_ordering_data.time_since_seen > wait_time:
                del face_orderings[face_ordering_idx]
            else:
                face_ordering_data.time_since_seen += delta
        