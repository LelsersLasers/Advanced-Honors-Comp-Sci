import pandas as pd
import numpy as np


# ---------------------------------------------------------------------------- #
class DataPath:
    SONG   = 'data/data.csv'
    ARTIST = 'data/data_by_artist.csv'
    YEAR   = 'data/data_by_year.csv'
    GENRE  = 'data/data_w_genres.csv'

def all_data(data_path):
    print(f"\nLoading data from {data_path}")
    
    data = pd.read_csv(data_path)

    print(f"Data shape: {data.shape}")
    print(f"Data head: {data.head()}")
    print(f"Data info: {data.info()}")
    print("Loaded data\n")
    return data
# ---------------------------------------------------------------------------- #


# ---------------------------------------------------------------------------- #
def scale(data_features, category):
    low = data_features[category].min()
    high = data_features[category].max()
    data_features[category] = (data_features[category] - low) / (high - low)
    return data_features


def predictor_data(data_path):
    # 12 input categories, 1 output category
    data = all_data(data_path)

    data_features = data.copy()

    unused_category = ['artists', 'explicit', 'id', 'mode', 'name', 'release_date']
    for category in unused_category: data_features.pop(category)
    for category in data_features.columns: data_features = scale(data_features, category)

    # predictor target
    data_labels = data_features.pop('popularity')

    print(f"\nPredictor data features head: {data_features.head()}")
    print(f"Predictor data features info: {data_features.info()}\n")

    data_features = np.asarray(data_features).astype(np.float32)

    return data, data_features, data_labels

def autoencoder_data(data_path):
    # 13 input categories
    data = all_data(data_path)

    data_features = data.copy()

    unused_category = ['artists', 'explicit', 'id', 'mode', 'name', 'release_date']
    for category in unused_category: data_features.pop(category)
    for category in data_features.columns: data_features = scale(data_features, category)

    print(f"\nAutoencoder data features head: {data_features.head()}")
    print(f"Autoencoder data features info: {data_features.info()}\n")

    data_features = np.asarray(data_features).astype(np.float32)

    return data, data_features