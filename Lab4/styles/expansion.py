import tensorflow as tf
import tensorflow.keras as keras
import tensorflow.keras.layers as layers
import tensorflow.keras.losses as losses
import tensorflow.keras.optimizers as optimizers
# import tensorflow.keras.activations as activations

print(f"\n\nTensorflow version: {tf.__version__}")


import json

import data
import distances
import similarity

# ---------------------------------------------------------------------------- #
TEST_INDEX = 17424 - 2

EPOCHS = 20
LEARNING_RATE = 0.0001

MODEL_PATH      = 'output/save-expansion/model'
HISTORY_PATH    = 'output/save-expansion/history.json'
EMBEDDINGS_PATH = 'output/save-expansion/embeddings.txt'
# ---------------------------------------------------------------------------- #


# ---------------------------------------------------------------------------- #
def make_model(data_features):
    normalize = layers.Normalization()
    normalize.adapt(data_features)
    
    # autoencoder style: inputs -> larger hidden -> output is same shape as inputs
    model = keras.Sequential([
        normalize,
        layers.Dense(25),
        layers.LeakyReLU(),
        layers.Dense(50),
        layers.LeakyReLU(),
        layers.Dense(50),
        layers.LeakyReLU(),
        layers.Dense(25),
        layers.LeakyReLU(),
        layers.Dense(13),
    ])

    loss = losses.MeanAbsoluteError()
    # loss = losses.MeanSquaredError()
    # loss = losses.CosineSimilarity()

    optimizer = optimizers.RMSprop(learning_rate=LEARNING_RATE)
    # optimizer = optimizers.Adam(learning_rate=LEARNING_RATE)

    model.compile(
        optimizer=optimizer,
        loss=loss,
        metrics=['mae', 'mse', 'cosine_similarity'],
    )
    print(model.summary())

    return model

def train():
    all_data, data_features = data.autoencoder_data(True)

    model = make_model(data_features)

    history = model.fit(data_features, data_features, epochs=EPOCHS)

    print(f"\nSaving model to {MODEL_PATH}...")
    model.save(MODEL_PATH)
    json.dump(history.history, open(HISTORY_PATH, 'w'), indent=4)
    print("Model saved\n")
# ---------------------------------------------------------------------------- #


# ---------------------------------------------------------------------------- #
def create_intermediate_model():
    # TODO: should also skip the normalization layer?
    
    model = keras.models.load_model(MODEL_PATH)
    # forward pass until the very last layer
    # skip any Dropout layers
    intermediate_model = keras.Sequential()
    for (i, layer) in enumerate(model.layers):
        if not isinstance(layer, keras.layers.Dropout) and i < len(model.layers) - 3:
            intermediate_model.add(layer)
    print(intermediate_model.summary())
    return intermediate_model

def embeddings():
    intermediate_model = create_intermediate_model()
    all_data, data_features = data.autoencoder_data(False)
    
    similarity.embeddings(intermediate_model, all_data, data_features, EMBEDDINGS_PATH)
# ---------------------------------------------------------------------------- #


# ---------------------------------------------------------------------------- #
def predict(index=TEST_INDEX, dist=distances.cos_dist, display=True):
    return similarity.predict(dist, embeddings_path=EMBEDDINGS_PATH, display=display, target_idx=index)
# ---------------------------------------------------------------------------- #
