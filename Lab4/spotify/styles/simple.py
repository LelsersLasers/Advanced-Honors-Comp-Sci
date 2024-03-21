import distances
import data

TEST_INDEX = 17424 - 2


# ---------------------------------------------------------------------------- #
def predict():
	all_data, data_features = data.autoencoder_data()

	print("Preparing data for prediction...")
	all_data_and_embeddings = [(all_data.iloc[i], data_features[i]) for i in range(len(all_data))]

	distances.predict(TEST_INDEX, distances.cos_dist, all_data_and_embeddings=all_data_and_embeddings)