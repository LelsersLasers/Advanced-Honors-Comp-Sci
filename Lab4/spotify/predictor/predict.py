import numpy as np


import distances
import predictor.consts


TEST_INDEX = 17424 - 2


# ---------------------------------------------------------------------------- #
import json

def load_embeddings():
    print("\nLoading embeddings...")
    all_data_and_embeddings = []
    with open(predictor.consts.EMBEDDINGS_PATH, 'r') as file:
        file.readline() # skip header
        for line in file:
            song_str, embedding_str = line.split('^^')
            song = json.loads(song_str.strip())
            embedding = np.array(json.loads(embedding_str.strip()))
            all_data_and_embeddings.append((song, embedding))
    return all_data_and_embeddings

def predict(target_idx):
	all_data_and_embeddings = load_embeddings()
	target_data_and_embedding = all_data_and_embeddings[target_idx]
    

	distances.predict(
        target_data_and_embedding,
		all_data_and_embeddings,
		distances.cos_dist
	)