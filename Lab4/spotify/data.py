import pandas as pd
import numpy as np

GENRE_TOP_POPULARITY = 2
GENRE_RANDOM_COUNT = 3


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
    unused_categories = ['artists', 'explicit', 'id', 'mode', 'name', 'release_date']
    for category in unused_categories: 
        try:
            all_features.pop(category)
        except KeyError:
            pass
    return all_features


def year_data():
    all_features = all_data(DataPath.YEAR)

    data_features = input_data_features(all_features.copy())
    data_features.pop('key')
    for category in data_features.columns: scale(data_features, category)

    print(f"\nYear data features shape: {data_features.shape}")
    print(f"Year data features head:\n{data_features.head()}\n")

    return data_features

def genre_data():
    all_features = all_data(DataPath.GENRE)
    data_features = input_data_features(all_features.copy())
    for category in data_features.columns: scale(data_features, category)

    genre_data = {}
    for i in range(data_features.shape[0]):
        genre = data_features.iloc[i]['genres']
        genre_data[genre] = data_features.iloc[i].drop('genres')

    genres = list(genre_data.keys())
    genres.sort(key=lambda x: genre_data[x]['popularity'], reverse=True)

    genre_idxs = [0, 1] + [np.random.randint(2, len(genres)) for _ in range(GENRE_RANDOM_COUNT)]
    genres_to_display = [genres[i] for i in genre_idxs]

    genre_data_dict = {} # genre_data_dict[category] = [category_data]
    for genre in genres_to_display:
        for key, value in genre_data[genre].items():
            if key not in genre_data_dict:
                genre_data_dict[key] = []
            genre_data_dict[key].append(value)

    return genres_to_display, genre_data_dict


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