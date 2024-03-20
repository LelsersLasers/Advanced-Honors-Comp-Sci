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
    
    all_features = pd.read_csv(data_path)

    print(f"Data shape: {all_features.shape}")
    print(f"Data head:\n{all_features.head()}")
    print("Loaded data\n")
    return all_features
# ---------------------------------------------------------------------------- #


# ---------------------------------------------------------------------------- #
def scale(data_features, category):
    low = data_features[category].min()
    high = data_features[category].max()
    data_features[category] = (data_features[category] - low) / (high - low)


def input_data_features(all_features):
    # 13 input categories as a pandas.DataFrame
    unused_categories = ['artists', 'explicit', 'id', 'mode', 'name', 'release_date']
    for category in unused_categories: all_features.pop(category)
    return all_features


def predictor_data(data_path):
    # 12 input categories, 1 output category
    all_features = all_data(data_path)

    data_features = input_data_features(all_features.copy())
    for category in data_features.columns: scale(data_features, category)

    # predictor target
    data_labels = data_features.pop('popularity')

    print(f"\nPredictor data features shape: {data_features.shape}")
    print(f"Predictor data features head:\n{data_features.head()}\n")

    data_features = np.asarray(data_features).astype(np.float32)

    return all_features, data_features, data_labels

def autoencoder_data(data_path):
    # 13 input categories
    all_features = all_data(data_path)

    data_features = input_data_features(all_features.copy())
    for category in data_features.columns: scale(data_features, category)

    print(f"\nAutoencoder data features shape: {data_features.shape}")
    print(f"Autoencoder data features head:\n{data_features.head()}\n")

    data_features = np.asarray(data_features).astype(np.float32)

    return all_features, data_features