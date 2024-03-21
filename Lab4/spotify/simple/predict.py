import distances
import data

TEST_INDEX = 17424 - 2


# ---------------------------------------------------------------------------- #
def predict(target_idx):
	all_data, data_features = data.autoencoder_data()

	target = data_features[target_idx]
	target_full = all_data.iloc[target_idx]

	print("Preparing data for prediction...")
	all_data_and_embeddings = [(all_data.iloc[i], data_features[i]) for i in range(len(all_data))]

	distances.predict(
		(target_full, target),
		all_data_and_embeddings,
		distances.cos_dist
	)