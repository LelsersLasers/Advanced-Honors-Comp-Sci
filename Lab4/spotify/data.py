import pandas as pd
import numpy as np


DATA_PATH = 'data/data.csv'
# MAX_POPULARITY = 100


def scale(data_features, category):
    low = data_features[category].min()
    high = data_features[category].max()
    data_features[category] = (data_features[category] - low) / (high - low)
    return data_features

def load_data():
    data = pd.read_csv(DATA_PATH)
    print(data.head())
    print(data.info())

    data_features = data.copy()

    # scale_pop = lambda x: x / MAX_POPULARITY
    # data_features['popularity'] = data_features['popularity'].apply(scale_pop)

    data_features.pop('artists')
    data_features.pop('explicit')
    data_features.pop('id')
    data_features.pop('mode')
    data_features.pop('name')
    data_features.pop('release_date')

    for category in data_features.columns:
        data_features = scale(data_features, category)
    
    # predictor target
    data_labels = data_features.pop('popularity')


    print(data_features.head())
    print(data_features.info())

    data_features = np.asarray(data_features).astype(np.float32)
    print(data_features)

    return data, data_features, data_labels
    # return data, data_features