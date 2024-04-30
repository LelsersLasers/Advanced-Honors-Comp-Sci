import data
import distances
import similarity

TEST_INDEX = 17424 - 2


# ---------------------------------------------------------------------------- #
def predict(index=TEST_INDEX, dist=distances.cos_dist, display=True):
	all_data, data_features = data.autoencoder_data(False)

	print("Preparing data for prediction...")
	all_data_and_embeddings = [(all_data.iloc[i], data_features[i]) for i in range(len(all_data))]

	return similarity.predict(index, dist, all_data_and_embeddings=all_data_and_embeddings, display=display)