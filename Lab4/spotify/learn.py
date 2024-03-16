

# ---------------------------------------------------------------------------- #
import pandas as pd
import numpy as np

np.set_printoptions(precision=3, suppress=True)
# ---------------------------------------------------------------------------- #


# ---------------------------------------------------------------------------- #
import tensorflow as tf
# import tensorflow.data as data
# import tensorflow.keras as keras
# import tensorflow.keras.utils as utils
import tensorflow.keras.layers as layers
# import tensorflow.keras.losses as losses
import tensorflow.keras.optimizers as optimizers
import tensorflow.keras.activations as activations

import tensorflow_similarity as tfsim
import tensorflow_similarity.losses as tfsim_losses

print(f"\n\nTensorflow version: {tf.__version__}")
print(f"TensorFlow Similarity version {tfsim.__version__}\n\n")
# ---------------------------------------------------------------------------- #


# ---------------------------------------------------------------------------- #
DATA_PATH = 'data/data/data.csv'

data = pd.read_csv(DATA_PATH)
print(data.head())
print(data.info())

data_features = data.copy()

data_labels = data_features.pop('popularity') # target

data_features.pop('artists')
data_features.pop('explicit')
data_features.pop('id')
data_features.pop('mode')
data_features.pop('name')

data_features["release_date"] = data_features["release_date"].apply(lambda x: int(x.split("-")[0]))

print(data_features.head())
print(data_features.info())

data_features = np.asarray(data_features).astype(np.float32)
print(data_features)
# ---------------------------------------------------------------------------- #


# ---------------------------------------------------------------------------- #
def make_model():
	normalize = layers.Normalization()
	normalize.adapt(data_features)

	inputs = layers.Input(shape=(data_features.shape[1],))
	x = normalize(inputs)
	x = layers.Dense(256, activation=activations.relu)(x)
	x = layers.Dense(256, activation=activations.relu)(x)
	x = layers.Dense(256, activation=activations.relu)(x)
	outputs = tfsim.layers.MetricEmbedding(100)(x)

	model = tfsim.models.SimilarityModel(inputs, outputs)
	return model

model = make_model()

optimizer = optimizers.Adam(learning_rate = 0.001)
loss = tfsim_losses.MultiSimilarityLoss(distance='cosine')

model.compile(
	optimizer=optimizer,
	loss=loss,
)

print(model.summary())
# ---------------------------------------------------------------------------- #


# ---------------------------------------------------------------------------- #
model.fit(
	data_features,
	data_labels,
	epochs=3
)
# ---------------------------------------------------------------------------- #