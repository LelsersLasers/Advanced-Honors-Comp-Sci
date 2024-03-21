import tensorflow as tf
import tensorflow.keras as keras
import tensorflow.keras.layers as layers
import tensorflow.keras.losses as losses
import tensorflow.keras.optimizers as optimizers
# import tensorflow.keras.activations as activations

print(f"\n\nTensorflow version: {tf.__version__}")

# TODO: argparse/inputs: epochs, activations


import data


EPOCHS = 10
MODEL_PATH = 'output/fullsave'
# ---------------------------------------------------------------------------- #


# ---------------------------------------------------------------------------- #
def make_model(data_features):
    normalize = layers.Normalization()
    normalize.adapt(data_features)
    
    # predictor style: inputs (12) -> hidden -> output (1) is single value from original inputs
    model = keras.Sequential([
        normalize,
        layers.Dense(8),
        layers.LeakyReLU(),
        layers.Dense(4),
        layers.LeakyReLU(),
        layers.Dense(1),
    ])
    # model = keras.Sequential([
    #     normalize,
    #     layers.Dense(50),
    #     layers.Dropout(0.3),
    #     layers.Dense(50),
    #     layers.Dropout(0.3),
    #     layers.Dense(25),
    #     layers.Dense(1),
    # ])

    loss = losses.MeanSquaredError()
    optimizer = optimizers.Adam()

    model.compile(optimizer=optimizer, loss=loss)
    print(model.summary())

    return model

def train(epochs):
    data_features, data_labels = data.predictor_data()

    model = make_model(data_features)

    model.fit(data_features, data_labels, epochs=epochs)

    print(f"\nSaving model to {MODEL_PATH}...")
    model.save(MODEL_PATH)
    print("Model saved")
# ---------------------------------------------------------------------------- #
