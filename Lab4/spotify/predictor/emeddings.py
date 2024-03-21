import tensorflow.keras as keras

import alive_progress
import numpy as np

import json
import data
import predictor.consts
# ---------------------------------------------------------------------------- #


# ---------------------------------------------------------------------------- #
def create_intermediate_model(model):
    # forward pass until the very last layer
    # skip any Dropout layers
    intermediate_model = keras.Sequential()
    for (i, layer) in enumerate(model.layers):
        if not isinstance(layer, keras.layers.Dropout) and i < len(model.layers) - 1:
            intermediate_model.add(layer)
    print(intermediate_model.summary())
    return intermediate_model


def emeddings():
    model = keras.models.load_model(predictor.consts.MODEL_PATH)
    intermediate_model = create_intermediate_model(model)

    all_data, data_features, _data_labels = data.predictor_data()

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
        with open(predictor.consts.EMBEDDINGS_PATH, 'w') as file:
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
