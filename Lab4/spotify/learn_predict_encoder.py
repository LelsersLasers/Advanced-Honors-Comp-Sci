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

    return data, data_features, data_labels

all_data, data_features, data_labels = load_data()
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

model.fit(data_features, data_labels, epochs=50)

model.save('output/try2-fullsave')
# ---------------------------------------------------------------------------- #

# ---------------------------------------------------------------------------- #
def extract_embedding(model, x):
    # forward pass until the very last layer
    intermediate_model = keras.Model(inputs=model.inputs, outputs=model.layers[-2].output)
    return intermediate_model(x)

def cosine_distance(a, b):
    return np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))

# test = '0.899,1926,0.995,["Louis Armstrong & His Hot Five"],0.614,189333,0.196,0,0jiH6Bf3OOm36ubMWZ0Sr5,0.892,4,0.0526,-14.019,1,Jazz Lips,9,1926,0.4270000000000001,201.11900000000003'
test = '0.285,2000,0.00239,["Coldplay"],0.429,266773,0.6609999999999999,0,3AJwUDP919kvQ9QcozQPxg,0.000121,11,0.234,-7.227,1,Yellow,84,2000-07-10,0.0281,173.372'
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

base_embedding = extract_embedding(model, x)
print(base_embedding)

print("Extracting all embeddings...")
all_embeddings = []
for i in range(len(data_features)):
    all_embeddings.append(extract_embedding(model, np.expand_dims(data_features[i], axis=0)))
print("Extracted all embeddings")

print("Sorting by cosine distance...")
angles = []
for i in range(len(all_embeddings)):
    b = np.squeeze(base_embedding.numpy(), axis=0)
    a = np.squeeze(all_embeddings[i].numpy(), axis=0)
    cos = cosine_distance(a, b)
    angle = np.arccos(cos) * 180 / np.pi
    angles.append(angle)
sorted_indices = np.argsort(angles)
print("Sorted by cosine distance")

print("Top 10 most similar songs:")
for i in range(20):
    ind = sorted_indices[i]
    angle = angles[ind]
    title = all_data.iloc[ind]['name']
    artist = all_data.iloc[ind]['artists']

    print(f"{i+1}. {title} by {artist} ({angle:.2f}°)")


