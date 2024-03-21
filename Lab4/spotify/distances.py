import alive_progress
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


TEST_INDEX = 17424 - 2


# ---------------------------------------------------------------------------- #
def predict(target_data_and_embedding, all_data_and_embeddings, dist_fn):
	target_data = target_data_and_embedding[0]
	target_embedding = target_data_and_embedding[1]
	# ------------------------------------------------------------------------ #
	print("Calculating distances...")
	dists = []
	song_count = len(all_data_and_embeddings)
	with alive_progress.alive_bar(song_count) as bar:
		for i in range(song_count):
			all_data_and_embedding = all_data_and_embeddings[i]
			other_embedding = all_data_and_embedding[1]
			all_data = all_data_and_embedding[0]
			dist = dist_fn(target_embedding, other_embedding)
			dists.append((dist, all_data))
			bar()
	dists.sort(key=lambda x: x[0], reverse=dist_fn.reverse_sort)
	# ------------------------------------------------------------------------ #

	# ------------------------------------------------------------------------ #
	print("Top 10 most similar songs:")
	print("BASE SONG:", target_data['name'], "by", target_data['artists'])
	for i in range(10):
		dist, song = dists[i]
		print(f"{i + 1}) {song['name']} by {song['artists']} (dist value: {dist:.3f})")
	# ------------------------------------------------------------------------ #