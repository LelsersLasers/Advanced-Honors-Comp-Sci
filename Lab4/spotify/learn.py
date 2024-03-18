EPOCHS = 20
MODEL_PATH = 'output/fullsave'


# ---------------------------------------------------------------------------- #
import data
all_data, data_features, data_labels = data.load_data()
# ---------------------------------------------------------------------------- #


# ---------------------------------------------------------------------------- #
import tensorflow as tf
# import tensorflow.data as data
import tensorflow.keras as keras
# import tensorflow.keras.utils as utils
import tensorflow.keras.layers as layers
import tensorflow.keras.losses as losses
import tensorflow.keras.optimizers as optimizers
import tensorflow.keras.activations as activations

print(f"\n\nTensorflow version: {tf.__version__}")


def make_model():
    normalize = layers.Normalization()
    normalize.adapt(data_features)
    
    model = keras.Sequential([
        normalize,
        layers.Dense(8),
        # layers.Dense(200),
        # layers.Dense(100),
        layers.Dense(4),
        layers.Dense(1),
    ])

    loss = losses.MeanSquaredError()
    optimizer = optimizers.Adam()

    model.compile(optimizer=optimizer, loss=loss)

    return model

model = make_model()
print(model.summary())

model.fit(data_features, data_labels, epochs=EPOCHS)
# ---------------------------------------------------------------------------- #


# ---------------------------------------------------------------------------- #
print(f"\nSaving model to {MODEL_PATH}...")
model.save(MODEL_PATH)
print("Model saved")
# ---------------------------------------------------------------------------- #