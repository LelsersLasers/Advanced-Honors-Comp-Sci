import alive_progress

import data
import distances


TEST_INDEX = 17424 - 2


# ---------------------------------------------------------------------------- #
def predict(target_idx):
	all_data, data_features = data.autoencoder_data()

	target = data_features[target_idx]
	target_full = all_data.iloc[target_idx]

	# ------------------------------------------------------------------------ #
	print("Calculating distances...")
	dists = []
	song_count = len(data_features)
	with alive_progress.alive_bar(song_count) as bar:
		for i in range(song_count):
			other = data_features[i]
			dist = distances.cosine_distance(target, other)
			dists.append((i, dist))
			bar()
	dists.sort(key=lambda x: x[1], reverse=True)
	# ------------------------------------------------------------------------ #

	# ------------------------------------------------------------------------ #
	print("Top 10 most similar songs:")
	print("BASE SONG:", target_full['name'], "by", target_full['artists'])
	for i in range(10):
		song_idx, dist = dists[i]
		angle = distances.cos_to_angle(dist)
		song = all_data.iloc[song_idx]
		print(f"{i + 1}) {song['name']} by {song['artists']} (cos: {dist:.3f}, ({angle:.2f}°)")
	# ------------------------------------------------------------------------ #