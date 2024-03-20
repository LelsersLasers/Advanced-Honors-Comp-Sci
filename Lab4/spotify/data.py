import pandas as pd
import numpy as np

BAR_GROUPS = 6


# ---------------------------------------------------------------------------- #
class DataPath:
    SONG   = 'data/data.csv'
    ARTIST = 'data/data_by_artist.csv'
    YEAR   = 'data/data_by_year.csv'
    GENRE  = 'data/data_by_genres.csv'

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
    try:
        low = data_features[category].min()
        high = data_features[category].max()
        data_features[category] = (data_features[category] - low) / (high - low)
    except TypeError:
        pass


def input_data_features(all_features):
    # 13 input categories as a pandas.DataFrame
    unused_categories = ['explicit', 'id', 'mode', 'name', 'release_date']
    for category in unused_categories: 
        try:
            all_features.pop(category)
        except KeyError:
            pass
    return all_features
# ---------------------------------------------------------------------------- #


# ---------------------------------------------------------------------------- #
def year_data():
    all_features = all_data(DataPath.YEAR)

    data_features = input_data_features(all_features.copy())
    data_features.pop('key')
    for category in data_features.columns: scale(data_features, category)

    print(f"\nYear data features shape: {data_features.shape}")
    print(f"Year data features head:\n{data_features.head()}\n")

    return data_features


def group_bar_graph_data(data_path, target):
    all_features = all_data(data_path)
    data_features = input_data_features(all_features.copy())
    for category in data_features.columns: scale(data_features, category)

    category_idxs = [np.random.randint(1, data_features.shape[0]) for _ in range(BAR_GROUPS)]
    category_data = {}
    for i in range(BAR_GROUPS):
        iloc = category_idxs[i]
        row = data_features.iloc[iloc]
        group = row[target]
        category_data[group] = row.drop(target)

    categories = list(category_data.keys())

    bar_data = {} # bar_data[category] = [category_data]
    for category in categories:
        for key, value in category_data[category].items():
            if key not in bar_data:
                bar_data[key] = []
            bar_data[key].append(value)

    return categories, bar_data

def genre_data():
    categories_to_display, bar_data = group_bar_graph_data(DataPath.GENRE, 'genres')
    return categories_to_display, bar_data

def artist_data():
    categories_to_display, bar_data = group_bar_graph_data(DataPath.ARTIST, 'artists')
    return categories_to_display, bar_data
# ---------------------------------------------------------------------------- #


# ---------------------------------------------------------------------------- #
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
# ---------------------------------------------------------------------------- #