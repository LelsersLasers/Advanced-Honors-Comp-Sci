import cv2
import argparse
import face_swap


ap = argparse.ArgumentParser()


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
ap.add_argument("-s", "--save", required=False, help="save output to path", default=None)
ap.add_argument("-d", "--debug", required=False, help="draw debug outlines", action="store_true")
ap.add_argument("-b", "--blur", required=False, help="enable blurring", action="store_true")
ap.add_argument(
    "-t",
    "--blur-thickness",
    required=False,
    help="blur thickness",
    default=40,
    type=int,
)
ap.add_argument("-r", "--blur-radius", required=False, help="blur strength (higher = lower fps)", default=15, type=int)
ap.add_argument(
    "-o",
    "--oval",
    required=False,
    help="cut out faces as ovals instead of rectangles",
    action="store_true",
)
ap.add_argument(
    "-w",
    "--wait-time",
    required=False,
    help="how long to wait before removing a face (only for `-i video/camera)`",
    default=0.4,
    type=float,
)
ap.add_argument(
    "-m",
    "--order-offset",
    required=False,
    help="face swap ordering offset",
    default=1,
    type=int,
)
ap.add_argument(
    "-q",
    "--quiet",
    required=False,
    help="no output window",
    action="store_true",
)
args = vars(ap.parse_args())

if (args["input"] == "image" or args["input"] == "video") and args["path"] is None:
    raise Exception("An image or video requires a path")


if not args["quiet"]:
    print("Press q to quit")

if args["input"] == "image":
    original_image = cv2.imread(args["path"])
    output_image = original_image.copy()
    face_swap.image_detection(original_image, args)
elif args["input"] == "video":
    original_video = cv2.VideoCapture(args["path"])
    face_swap.video_detection(original_video, args)
elif args["input"] == "camera":
    if args["path"] is None:
        original_video = cv2.VideoCapture(0)
    else:
        original_video = cv2.VideoCapture(args["path"])
    face_swap.video_detection(original_video, args)
