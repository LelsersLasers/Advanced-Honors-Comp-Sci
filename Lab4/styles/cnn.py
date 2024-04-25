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

EPOCHS = 8
LEARNING_RATE = 0.001

IMAGE_SIZE = (128, 128)


GOOGLE_MODEL_PATH    = 'output/save-cnn/google/model'
ALBUM_ART_MODEL_PATH = 'output/save-cnn/album_art/model'

GOOGLE_HISTORY_PATH    = 'output/save-cnn/google/history.json'
ALBUM_ART_HISTORY_PATH = 'output/save-cnn/album_art/history.json'

GOOGLE_EMBEDDINGS_PATH    = 'output/save-cnn/google/embeddings.txt'
ALBUM_ART_EMBEDDINGS_PATH = 'output/save-cnn/album_art/embeddings.txt'
# ---------------------------------------------------------------------------- #


# ---------------------------------------------------------------------------- #
def make_model():
    # predictor style: (128x128 image) -> hidden -> output (13) is inputs
    
    # (128) -> 42 -> 21 -> 10
    # 1000 -> 256 -> 64 -> (13)
    # (128 - 5) / 3 + 1 = 42
    # ( 42 - 2) / 2 + 1 = 21
    # ( 21 - 3) / 2 + 1 = 10
    model = keras.Sequential([
        layers.Conv2D(
            filters = 10,
            kernel_size = 3,
            strides = 1,
            input_shape = IMAGE_SIZE + (3,),
            # activation = activations.relu,
            padding = "same",
        ),
        layers.LeakyReLU(),
        layers.BatchNormalization(),

        layers.Conv2D(
            filters = 10,
            kernel_size = 3,
            strides = 1,
            input_shape = IMAGE_SIZE + (3,),
            # activation = activations.relu,
            padding = "same",
        ),
        layers.LeakyReLU(),
        layers.BatchNormalization(),
        
        layers.Conv2D(
            filters = 10,
            kernel_size = 5,
            strides = 3,
            # activation = activations.relu,
        ),
        layers.LeakyReLU(),
        layers.BatchNormalization(),
        
        layers.MaxPool2D(
            pool_size = 2,
            strides = 2,
        ),
          
        layers.Conv2D(
            filters = 10,
            kernel_size = 3,
            strides = 2,
            # activation = activations.relu,
        ),
        layers.LeakyReLU(),
        layers.BatchNormalization(),
          
        layers.Flatten(),
        
        layers.Dense(256),
        layers.LeakyReLU(),
        layers.Dropout(0.3),
        
        layers.Dense(64),
        layers.LeakyReLU(),
        layers.Dropout(0.3),
        
        layers.Dense(13),
    ])

    # loss = losses.MeanSquaredError()
    loss = losses.MeanAbsoluteError()
    # loss = losses.CosineSimilarity()

    # optimizer = optimizers.Adam(learning_rate=LEARNING_RATE)
    optimizer = optimizers.RMSprop(learning_rate=LEARNING_RATE)

    model.compile(
        optimizer=optimizer,
        loss=loss,
        metrics=['mse', 'mae', 'cosine_similarity'],
    )
    print(model.summary())

    return model

def train(google_mode):
    _all_data, train_ds, _images = data.cnn_data(google_mode)

    model = make_model()

    history = model.fit(train_ds, epochs=EPOCHS)

    model_path = GOOGLE_MODEL_PATH if google_mode else ALBUM_ART_MODEL_PATH
    print(f"\nSaving model to {model_path}...")
    model.save(model_path)

    history_path = GOOGLE_HISTORY_PATH if google_mode else ALBUM_ART_HISTORY_PATH
    json.dump(history.history, open(history_path, 'w'))
    print("Model saved\n")
# ---------------------------------------------------------------------------- #


# ---------------------------------------------------------------------------- #
def create_intermediate_model(google_mode):
    # TODO: should also skip the normalization layer?

    model_path = GOOGLE_MODEL_PATH if google_mode else ALBUM_ART_MODEL_PATH
    model = keras.models.load_model(model_path)
    # forward pass until the very last layer
    # skip any Dropout layers
    intermediate_model = keras.Sequential()
    for (i, layer) in enumerate(model.layers):
        # and not isinstance(layer, keras.layers.BatchNormalization)
        if not isinstance(layer, keras.layers.Dropout) and i < len(model.layers) - 1:
            intermediate_model.add(layer)
    print(intermediate_model.summary())
    return intermediate_model

def embeddings(google_mode):
    intermediate_model = create_intermediate_model(google_mode)
    all_data, _train_ds, images = data.cnn_data(google_mode)
    
    embeddings_path = GOOGLE_EMBEDDINGS_PATH if google_mode else ALBUM_ART_EMBEDDINGS_PATH
    similarity.embeddings(intermediate_model, all_data, images, embeddings_path)
# ---------------------------------------------------------------------------- #


# ---------------------------------------------------------------------------- #
def predict(google_mode):
    embeddings_path = GOOGLE_EMBEDDINGS_PATH if google_mode else ALBUM_ART_EMBEDDINGS_PATH
    similarity.predict(TEST_INDEX, distances.cos_dist, embeddings_path=embeddings_path)
# ---------------------------------------------------------------------------- #
