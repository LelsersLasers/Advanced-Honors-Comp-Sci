import alive_progress
import numpy as np

import json


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
def load_embeddings(embeddings_path):
    print("\nLoading embeddings...")
    all_data_and_embeddings = []
    with open(embeddings_path, 'r') as file:
        file.readline() # skip header
        for line in file:
            song_str, embedding_str = line.split('^^')
            song = json.loads(song_str.strip())
            embedding = np.array(json.loads(embedding_str.strip()))
            all_data_and_embeddings.append((song, embedding))
    return all_data_and_embeddings


def predict(target_idx, embeddings_path, dist_fn):   
	all_data_and_embeddings = load_embeddings(embeddings_path)
	
	target_data_and_embedding = all_data_and_embeddings[target_idx]
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
# ---------------------------------------------------------------------------- #
		

# ---------------------------------------------------------------------------- #
def emeddings(intermediate_model, all_data, data_features, embeddings_path):
    # ------------------------------------------------------------------------ #
    print("\nCalculating all embeddings...")
    all_embeddings = []
    song_count = all_data.shape[0]
    with alive_progress.alive_bar(song_count) as bar:
        for i in range(song_count):
            x = np.expand_dims(data_features[i], axis=0)

            embedding = intermediate_model(x)
            embedding = np.squeeze(embedding.numpy(), axis=0)
            
            pair = (all_data.iloc[i], embedding)
            all_embeddings.append(pair)
            bar()
    print("Calculated all embeddings\n")
    # ------------------------------------------------------------------------ #

    # ------------------------------------------------------------------------ #
    print("\nWriting embeddings to file...")
    with alive_progress.alive_bar(song_count) as bar:
        with open(embeddings_path, 'w') as file:
            file.write("id ^^ embedding\n")
            for i in range(song_count):
                song, embedding = all_embeddings[i]
                song_dict = song.to_dict()
                song_str = json.dumps(song_dict)
                embedding_str = json.dumps(embedding.tolist())
                file.write(f"{song_str} ^^ {embedding_str}\n")
                bar()
    print("Wrote embeddings to file\n")
    # ------------------------------------------------------------------------ #
# ---------------------------------------------------------------------------- #