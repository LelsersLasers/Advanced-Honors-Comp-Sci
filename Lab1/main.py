import numpy as np
import argparse
import cv2
import sys
import time

# ---------------------------------------------------------------------------- #
"""
- Image basics: saving/loading
- Drawing: rectangle in debug mode
- Image processing: crop + resize
- Smoothing and blurring: TODO
- Face dectect
- Video/camera
- Grabcut forground extraction: TODO?

TODO:
- Face mapping order
    - Command + stable as face size changes
    - Map each face to a number and the number to the center of the face
    - Organize faces that minimizes the total distance between the new centers of the face and the old centers of the face
- Cut faces out as ovals
    - +Play nice with blurring
- Smoothing and blurring: WIP
    - Create blurred version of output frame
    - Create mask for the outline of the pasted face
    - Used blurred image on masked areas, and original on non-masked areas
    - Make argparse option
        - `-r` or `--radius` for blur radius in blur function
        - `-t` or `--thickness` for blur thickness for mask
        - `-b` or `--blur` to enable blurring
            - Or maybe for how many "layers"?
    - Make it blur in "layers"
        - Blur the edges with a very strong blur, then blur the surrounding area with a weaker blur
- Forground extraction: Worth it? (Very slow, and iffy)
    - Expand the face rect by ~40 percent in all directions
        - Make argparse option?
    - https://www.geeksforgeeks.org/python-foreground-extraction-in-an-image-using-grabcut-algorithm/
- Save video - fourcc

"""

# ---------------------------------------------------------------------------- #
modelFile = "models/res10_300x300_ssd_iter_140000_fp16.caffemodel"
configFile = "models/deploy.prototxt"
net = cv2.dnn.readNetFromCaffe(configFile, modelFile)


class Face:
    def __init__(self, x, y, w, h):
        self.x = x
        self.y = y
        self.w = w
        self.h = h

        self.center_x = self.x + self.w / 2
        self.center_y = self.y + self.h / 2

    def calc_area(self):
        return self.w * self.h

    def __str__(self):
        return f"Face at {self.center}"

    def __repr__(self):
        return f"Face({self.x}, {self.y}, {self.w}, {self.h})"

    def draw(self, image, color=(255, 0, 0)):
        # rect outline
        cv2.rectangle(
            image, (self.x, self.y), (self.x + self.w, self.y + self.h), color, 2
        )


def detect_faces(image, conf):
    faces = detect_faces_dnn(image, conf)
    faces.sort(key=Face.calc_area, reverse=True)

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

            w = x2 - x1
            h = y2 - y1

            # Grapcut 1
            # expanded_w = int(w * 1.4)
            # expanded_h = int(h * 1.4)

            # x = max(0, x1 - int((expanded_w - w) / 2))
            # y = max(0, y1 - int((expanded_h - h) / 2))

            # detected_faces.append(Face(x, y, expanded_w, expanded_h))
            detected_faces.append(Face(x1, y1, w, h))

    return detected_faces


# ---------------------------------------------------------------------------- #
def combine_with_mask(image1, image2, mask):
    # Where mask == true => image2, else image1
    inverse_mask = cv2.bitwise_not(mask)
    result = cv2.bitwise_and(image1, image1, mask=inverse_mask)
    image2_part = cv2.bitwise_and(image2, image2, mask=mask)
    final_result = cv2.add(result, image2_part)

    return final_result


def swap_faces(original_image, output_image, faces, oval):
    for i, face in enumerate(faces):
        try:
            face_crop = original_image[
                face.y : face.y + face.h, face.x : face.x + face.w
            ]
            next_face = faces[(i + 1) % len(faces)]
            face_resized = cv2.resize(face_crop, (next_face.w, next_face.h))

            if oval:
                oval_mask = np.zeros(face_resized.shape[:2], np.uint8)
                cv2.ellipse(
                    oval_mask,
                    (int(next_face.w / 2), int(next_face.h / 2)),
                    (int(next_face.w / 2), int(next_face.h / 2)),
                    0,
                    0,
                    360,
                    (255, 255, 255),
                    -1,
                )
                face_resized = cv2.bitwise_and(
                    face_resized, face_resized, mask=oval_mask
                )

                output_image[
                    next_face.y : next_face.y + next_face.h,
                    next_face.x : next_face.x + next_face.w,
                ] = combine_with_mask(
                    output_image[
                        next_face.y : next_face.y + next_face.h,
                        next_face.x : next_face.x + next_face.w,
                    ],
                    face_resized,
                    oval_mask,
                )
            else:
                output_image[
                    next_face.y : next_face.y + next_face.h,
                    next_face.x : next_face.x + next_face.w,
                ] = face_resized

            # Grapcut 2
            # mask = np.zeros(face_resized.shape[:2], np.uint8)
            # bgdModel = np.zeros((1,65), np.float64)
            # fgdModel = np.zeros((1,65), np.float64)
            # rect = (1, 1, next_face.w, next_face.h)

            # cv2.grabCut(face_resized, mask, rect, bgdModel, fgdModel, 5, cv2.GC_INIT_WITH_RECT)

            # # Use cv2.GC_PR_FGD to get the foreground
            # mask2 = np.where((mask==cv2.GC_PR_FGD)|(mask == cv2.GC_FGD),0,1).astype('uint8')

            # face_grapcut = face_resized * mask2[:, :, np.newaxis]
            # cv2.imshow("face_grapcut", face_grapcut)

        except:
            pass


def blur_edges(output_image, faces, blur_thickness, blur_radius, oval):
    # blurred_image = cv2.blur(output_image, (51, 51))

    if blur_radius % 2 == 0:
        blur_radius += 1
    blurred_image = cv2.medianBlur(output_image, blur_radius)

    mask = np.zeros(output_image.shape[:2], np.uint8)

    for face in faces:
        if oval:
            cv2.ellipse(
                mask,
                (int(face.center_x), int(face.center_y)),
                (int(face.w / 2), int(face.h / 2)),
                0,
                0,
                360,
                (255, 255, 255),
                blur_thickness,
            )
        else:
            cv2.rectangle(
                mask,
                (face.x, face.y),
                (face.x + face.w, face.y + face.h),
                (255, 255, 255),
                blur_thickness,
            )

    final_result = combine_with_mask(output_image, blurred_image, mask)

    return final_result


def double_blur_edges(output_image, faces, blur_thickness, blur_radius, oval):
    output_image = blur_edges(output_image, faces, blur_thickness, blur_radius, oval)
    output_image = blur_edges(
        output_image, faces, blur_thickness // 2, blur_radius * 2, oval
    )

    return output_image


def video_detection(orginal_video, args):
    if not orginal_video.isOpened():
        raise Exception("Could not open video")

    if args["save"] is not None:
        fps = orginal_video.get(cv2.CAP_PROP_FPS)
        width = int(orginal_video.get(cv2.CAP_PROP_FRAME_WIDTH))
        height = int(orginal_video.get(cv2.CAP_PROP_FRAME_HEIGHT))

        fourcc = (
            int(orginal_video.get(cv2.CAP_PROP_FOURCC))
            .to_bytes(4, byteorder=sys.byteorder)
            .decode()
        )

        output_video = cv2.VideoWriter(
            args["save"], cv2.VideoWriter_fourcc(*fourcc), fps, (width, height)
        )

    while orginal_video.isOpened():
        ret, frame = orginal_video.read()

        if not ret:
            break

        output_frame = frame.copy()
        faces = detect_faces(frame, args["confidence"])
        swap_faces(frame, output_frame, faces, args["oval"])
        if args["blur"]:
            output_frame = double_blur_edges(
                output_frame,
                faces,
                args["blur_thickness"],
                args["blur_radius"],
                args["oval"],
            )

        if args["debug"]:
            for face in faces:
                face.draw(output_frame)

        if args["save"] is not None:
            output_video.write(output_frame)

        cv2.imshow("Output", output_frame)

        if cv2.waitKey(1) & 0xFF == ord("q"):
            break

    orginal_video.release()

    if args["save"] is not None:
        output_video.release()

    cv2.destroyAllWindows()


def image_detection(original_image, args):
    output_image = original_image.copy()
    faces = detect_faces(original_image, args["confidence"])

    if len(faces) < 2:
        raise Exception(
            f"Not enough faces detected. {len(faces)} detected, at least 2 required."
        )

    swap_faces(original_image, output_image, faces, args["oval"])

    if args["blur"]:
        output_image = double_blur_edges(
            output_image,
            faces,
            args["blur_thickness"],
            args["blur_radius"],
            args["oval"],
        )

    if args["debug"]:
        for face in faces:
            face.draw(output_image)

    if args["save"] is not None:
        cv2.imwrite(args["save"], output_image)

    cv2.imshow("Output", output_image)

    cv2.waitKey(10_000)


# ---------------------------------------------------------------------------- #


# ---------------------------------------------------------------------------- #
ap = argparse.ArgumentParser()


# TODO: use type=
# TODO: clean, clarify, and expand wordings/help messages
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
    "-s", "--save", required=False, help="save output to path", default=None
)
ap.add_argument(
    "-d", "--debug", required=False, help="draw debug outlines", action="store_true"
)
ap.add_argument(
    "-b", "--blur", required=False, help="enable blurring", action="store_true"
)
ap.add_argument(
    "-t",
    "--blur-thickness",
    required=False,
    help="blur thickness",
    default=40,
    type=int,
)
ap.add_argument(
    "-r", "--blur-radius", required=False, help="blur strength", default=21, type=int
)

ap.add_argument(
    "-o",
    "--oval",
    required=False,
    help="cut out faces as ovals instead of rectangles",
    action="store_true",
)
# TODO: command for face mapping order?
args = vars(ap.parse_args())

if (args["input"] == "image" or args["input"] == "video") and args["path"] is None:
    raise Exception("An image or video requires a path")


print("Press q to quit")

if args["input"] == "image":
    original_image = cv2.imread(args["path"])
    output_image = original_image.copy()
    image_detection(original_image, args)
elif args["input"] == "video":
    original_video = cv2.VideoCapture(args["path"])
    video_detection(original_video, args)
elif args["input"] == "camera":
    if args["path"] is None:
        original_video = cv2.VideoCapture(0)
    else:
        original_video = cv2.VideoCapture(args["path"])
    time.sleep(0.1)
    video_detection(original_video, args)
