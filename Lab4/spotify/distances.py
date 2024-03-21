import numpy as np


# ---------------------------------------------------------------------------- #
def cosine_distance(a, b):
    return np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))

def euclidean_distance(a, b):
	return np.linalg.norm(a - b)

def manhattan_distance(a, b):
	return np.sum(np.abs(a - b))

def dot_product(a, b):
	return np.dot(a, b)
# ---------------------------------------------------------------------------- #


# ---------------------------------------------------------------------------- #
def cos_to_angle(cos):
	cos = clamp(cos, -1, 1)
	return np.arccos(cos) * 180 / np.pi

def clamp(x, a, b):
    return max(a, min(b, x))
# ---------------------------------------------------------------------------- #