import numpy as np

# ---------------------------------------------------------------------------- #
class DistFn:
    def __init__(self, fn, reverse_sort):
        self.fn = fn
        self.reverse_sort = reverse_sort
    def __call__(self, a, b):
        return self.fn(a, b)
    
cos_dist       = DistFn(lambda a, b: np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b)), True)
euclidean_dist = DistFn(lambda a, b: np.linalg.norm(a - b), False)
manhattan_dist = DistFn(lambda a, b: np.sum(np.abs(a - b)), False)
dot_product    = DistFn(lambda a, b: np.dot(a, b), True)
# ---------------------------------------------------------------------------- #


# ---------------------------------------------------------------------------- #
def cos_to_angle(cos):
    cos = clamp(cos, -1, 1)
    return np.arccos(cos) * 180 / np.pi

def clamp(x, a, b):
    return max(a, min(b, x))
# ---------------------------------------------------------------------------- #