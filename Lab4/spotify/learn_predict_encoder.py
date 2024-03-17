# ---------------------------------------------------------------------------- #
import pandas as pd
import numpy as np

np.set_printoptions(precision=3, suppress=True)

DATA_PATH = 'data/data.csv'
MAX_POPULARITY = 100


def load_data():
    data = pd.read_csv(DATA_PATH)
    print(data.head())
    print(data.info())

    data_features = data.copy()

    scale_pop = lambda x: x / MAX_POPULARITY
    data_features['popularity'] = data_features['popularity'].apply(scale_pop)

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

    return data_features, data_labels

data_features, data_labels = load_data()
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
        layers.Dense(64, activation='relu'),
        layers.Dense(64, activation='relu'),
        layers.Dense(1), # linear regression so no activation
    ])

    loss = losses.MeanSquaredError()
    optimizer = optimizers.Adam()

    model.compile(optimizer=optimizer, loss=loss)

    return model

model = make_model()

model.fit(data_features, data_labels, epochs=10)

model.save('output/try2-fullsave')
# ---------------------------------------------------------------------------- #

# ---------------------------------------------------------------------------- #
def extract_embedding(model, x):
    # forward pass until the very last layer
    intermediate_model = keras.Model(inputs=model.inputs, outputs=model.layers[-2].output)
    return intermediate_model(x)

test = '0.899,1926,0.995,["Louis Armstrong & His Hot Five"],0.614,189333,0.196,0,0jiH6Bf3OOm36ubMWZ0Sr5,0.892,4,0.0526,-14.019,1,Jazz Lips,9,1926,0.4270000000000001,201.11900000000003'

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
speechiness = float(test[17])
tempo = float(test[18])

x = np.array([valence, year, acousticness, danceability, duration_ms, energy, instrumentalness, key, liveness, loudness, speechiness, tempo], dtype=np.float32)
x = np.expand_dims(x, axis=0)
print(x)

embedding = extract_embedding(model, x)
print(embedding)



