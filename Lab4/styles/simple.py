import alive_progress

import data
import distances
import similarity

TEST_INDEX = 17424 - 2


# ---------------------------------------------------------------------------- #
def predict(index=TEST_INDEX, dist=distances.cos_dist, display=True, extra_categories_to_remove=None):
    all_data, data_features = data.autoencoder_data(False, extra_categories_to_remove)

    print("Preparing data for prediction...")
    all_data_and_embeddings = []
    song_count = len(all_data)
    with alive_progress.alive_bar(song_count) as bar:
        for i in range(song_count):
            song = all_data.iloc[i]
            embedding = data_features[i]
            all_data_and_embeddings.append((song, embedding))
            bar()

    return similarity.predict(dist, all_data_and_embeddings=all_data_and_embeddings, display=display, target_idx=index)