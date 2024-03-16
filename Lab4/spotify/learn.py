

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
DATA_PATH = 'data/data.csv'

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
data_features.pop('release_date')


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
	epochs=5,
)

model.save('output/try1-fullsave')
# ---------------------------------------------------------------------------- #


# valence,year,acousticness,artists,danceability,duration_ms,energy,explicit,id,instrumentalness,key,liveness,loudness,mode,name,popularity,release_date,speechiness,tempo
test='0.606,2009,0.00244,["Rascal Flatts"],0.562,276707,0.91,0,5YbeJyTQkdSAWe1Ie4sLAl,0.0,5,0.0676,-6.939,1,"Life is a Highway - From ""Cars""",56,2009-01-01,0.058,103.057'
test = test.split(',')

valence = float(test[0])
year = float(test[1])
acousticness = float(test[2])
danceability = float(test[4])
duration_ms = float(test[5])
energy = float(test[6])
instrumentalness = float(test[9])
key = float(test[10])
liveness = float(test[11])
loudness = float(test[12])
speechiness = float(test[16])
tempo = float(test[17])

x = np.array([valence, year, acousticness, danceability, duration_ms, energy, instrumentalness, key, liveness, loudness, speechiness, tempo], dtype=np.float32)
closest = model.lookup(x, k=5)

print(closest)


