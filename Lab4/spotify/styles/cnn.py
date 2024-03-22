import tensorflow as tf
import tensorflow.keras as keras
import tensorflow.keras.layers as layers
import tensorflow.keras.losses as losses
import tensorflow.keras.optimizers as optimizers
import tensorflow.keras.activations as activations

print(f"\n\nTensorflow version: {tf.__version__}")


import json

import data
import distances
import similarity

# ---------------------------------------------------------------------------- #
TEST_INDEX = 616 - 2

EPOCHS = 10
LEARNING_RATE = 0.0003

IMAGE_SIZE = (128, 128)

MODEL_PATH      = 'output/save-cnn'
HISTORY_PATH    = 'output/save-cnn/history.json'
EMBEDDINGS_PATH = 'output/save-cnn/embeddings.txt'
# ---------------------------------------------------------------------------- #


# ---------------------------------------------------------------------------- #
def make_model():
    # predictor style: (128x128 image) -> hidden -> output (13) is inputs
    
	# 128 -> 42 -> 21 -> 10
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
			activation = activations.relu,
			padding = "same",
		),
        layers.BatchNormalization(),

        layers.Conv2D(
			filters = 10,
			kernel_size = 3,
			strides = 1,
			activation = activations.relu,
			padding = "same",
		),
        layers.BatchNormalization(),
        
		layers.Conv2D(
			filters = 10,
			kernel_size = 5,
			strides = 3,
			activation = activations.relu,
		),
		layers.BatchNormalization(),
        
		layers.MaxPool2D(
			pool_size = 2,
			strides = 2,
		),
          
		layers.Conv2D(
			filters = 10,
			kernel_size = 3,
			strides = 2,
			activation = activations.relu,
		),
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

    loss = losses.MeanSquaredError()
    optimizer = optimizers.Adam(learning_rate=LEARNING_RATE)

    model.compile(optimizer=optimizer, loss=loss)
    print(model.summary())

    return model

def train():
    _all_data, album_art, data_features = data.cnn_data()

    model = make_model()

    history = model.fit(album_art, data_features, epochs=EPOCHS)

    print(f"\nSaving model to {MODEL_PATH}...")
    model.save(MODEL_PATH)
    json.dump(history.history, open(HISTORY_PATH, 'w'))
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
        if not isinstance(layer, keras.layers.Dropout) and i < len(model.layers) - 4:
            intermediate_model.add(layer)
    print(intermediate_model.summary())
    return intermediate_model

def embeddings():
    intermediate_model = create_intermediate_model()
    all_data, album_art, _data_features = data.cnn_data()
    
    similarity.embeddings(intermediate_model, all_data, album_art, EMBEDDINGS_PATH)
# ---------------------------------------------------------------------------- #


# ---------------------------------------------------------------------------- #
def predict():
	similarity.predict(TEST_INDEX, distances.cos_dist, embeddings_path=EMBEDDINGS_PATH)
# ---------------------------------------------------------------------------- #
