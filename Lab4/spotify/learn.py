import pandas as pd
import numpy as np

np.set_printoptions(precision=3, suppress=True)

import tensorflow as tf
# import tensorflow.data as data
import tensorflow.keras as keras
import tensorflow.keras.utils as utils
import tensorflow.keras.layers as layers
import tensorflow.keras.losses as losses
import tensorflow.keras.optimizers as optimizers
import tensorflow.keras.activations as activations


DATA_PATH = 'data/data/data.csv'


data = pd.read_csv(DATA_PATH)
# print(data.head())
# print(data.info())

data_features = data.copy()

# - Don't need: artists, explicit, id, mode, name
# - Build similarity based on popularity

data_labels = data_features.pop('popularity') # target

data_features.pop('artists')
data_features.pop('explicit')
data_features.pop('id')
data_features.pop('mode')
data_features.pop('name')

# print(data_features.head())
# print(data_features.info())

data_features = np.array(data_features)
print(data_features)



normalize = layers.Normalization()
normalize.adapt(data_features)

model = keras.Sequential([
	normalize,
	layers.Dense(64, activation=activations.relu),
	layers.Dense(64, activation=activations.relu),
	layers.Dense(1)
])

optimizer = optimizers.Adam(learning_rate = 0.001)
loss = losses.CategoricalCrossentropy()

model.compile(
	optimizer=optimizer,
	loss=loss,
	metrics=['accuracy']
)

model.fit(
	data_features,
	data_labels,
	epochs=3
)