import numpy as np
import cv2

def translate(image, x, y):
    M = np.float32([
        [1, 0, x],
        [0, 1, y]
    ])
    shifted = cv2.warpAffine(image, M, (image.shape[1], image.shape[0]))
    return shifted


def rotate(image, angle, center=None, scale=1.0):
    # angle: degrees
    (h, w) = image.shape[:2]
    if center is None:
        center = (w // 2, h // 2)

    M = cv2.getRotationMatrix2D(center, angle, scale)
    rotated = cv2.waitKeyarpAffine(image, M, (w, h))
    return rotated

def resize(image, width=None, height=None, inter=cv2.INTER_AREA):
    dim = None
    (h, w) = image.shape[:2]

    if width is None and height is None:
        return image

    elif width is None:
        r = height / float(h)
        dim = (int(w * r), height)
    else:
        r = width / float(w)
        dim = (width, int(h * r))

    resized = cv2.resize(image, dim, interpolation=inter)
    return resized

def flip(image, x=False, y=False):
    flipCode = None
    match (x, y):
        case (True, True): flipCode = -1
        case (True, False): flipCode = 1
        case (False, True): flipCode = 0
        case _: return image

    flipped = cv2.flip(image, flipCode)
    return flipped