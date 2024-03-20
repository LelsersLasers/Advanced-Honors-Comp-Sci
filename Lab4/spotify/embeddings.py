MODEL_PATH = 'output/fullsave'

# NOTE: the file ends in .csv but the seperators are " ^^ " which is not a standard csv seperator
EMBEDDINGS_PATH = 'output/embeddings.csv'


# ---------------------------------------------------------------------------- #
import alive_progress
import numpy as np
# ---------------------------------------------------------------------------- #


# ---------------------------------------------------------------------------- #
import data
all_data, data_features, _data_labels = data.predictor_data(data.DataPath.SONG)
# all_data, data_features = data.autoencoder_data(data.DataPath.SONG)
# ---------------------------------------------------------------------------- #


# ---------------------------------------------------------------------------- #
import tensorflow.keras as keras


def intermediate_model(model):
    # forward pass until the very last layer
    # skip any Dropout layers
    intermediate_model = keras.Sequential()
    for layer in model.layers:
        if not isinstance(layer, keras.layers.Dropout):
            intermediate_model.add(layer)
    intermediate_model.layers = intermediate_model.layers[:-1]
    return intermediate_model


model = keras.models.load_model(MODEL_PATH)
intermediate_model = intermediate_model(model)


print("\nExtracting all embeddings...")
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
print("Extracted all embeddings")
# ---------------------------------------------------------------------------- #


# ---------------------------------------------------------------------------- #
import json

print("\nWriting embeddings to file...")
with alive_progress.alive_bar(song_count) as bar:
    with open(EMBEDDINGS_PATH, 'w') as file:
        file.write("id ^^ embedding\n")
        for i in range(song_count):
            song, embedding = all_embeddings[i]
            song_dict = song.to_dict()
            song_str = json.dumps(song_dict)
            embedding_str = json.dumps(embedding.tolist())
            file.write(f"{song_str} ^^ {embedding_str}\n")
            bar()
print("Wrote embeddings to file")
# ---------------------------------------------------------------------------- #
