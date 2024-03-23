import alive_progress

import pandas as pd
import numpy as np

import spotipy
import spotipy.oauth2
import urllib
import cv2
import os
import dotenv

import tqdm
import multiprocessing
CHUNK_SIZE = 100

BAR_GROUPS = 6

IMAGE_SIZE = (128, 128)

IMAGE_DIR = 'output/save-cnn/images'


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


def remove_columns(all_features, unused_categories):
    # 13 input categories as a pandas.DataFrame + genre and artists
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

    data_features = remove_columns(
        all_features.copy(),
        ['explicit', 'id', 'mode', 'name', 'release_date', 'key', 'artists']
    )
    for category in data_features.columns: scale(data_features, category)

    print(f"\nYear data features shape: {data_features.shape}")
    print(f"Year data features head:\n{data_features.head()}\n")

    return data_features


def group_bar_graph_data(data_path, target):
    all_features = all_data(data_path)
    
    data_features = remove_columns(
        all_features.copy(),
        ['explicit', 'id', 'mode', 'name', 'release_date']
    )
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
def predictor_data():
    # 12 input categories, 1 output category
    all_features = all_data(DataPath.SONG)

    data_features = remove_columns(
        all_features.copy(),
        ['explicit', 'id', 'mode', 'name', 'release_date', 'artists', 'genre']
    )
    for category in data_features.columns: scale(data_features, category)

    # predictor target
    data_labels = data_features.pop('popularity')

    print(f"\nPredictor data features shape: {data_features.shape}")
    print(f"Predictor data features head:\n{data_features.head()}\n")

    data_features = np.asarray(data_features).astype(np.float32)

    return all_features, data_features, data_labels

def autoencoder_data():
    # 13 input categories
    all_features = all_data(DataPath.SONG)

    data_features = remove_columns(
        all_features.copy(),
        ['explicit', 'id', 'mode', 'name', 'release_date', 'artists', 'genre']
    )
    for category in data_features.columns: scale(data_features, category)

    print(f"\nAutoencoder data features shape: {data_features.shape}")
    print(f"Autoencoder data features head:\n{data_features.head()}\n")

    data_features = np.asarray(data_features).astype(np.float32)

    return all_features, data_features

def cnn_data():
    env = dotenv.dotenv_values('.env')
    spotify_client = env['SPOTIPY_CLIENT']
    spotify_secret = env['SPOTIPY_SECRET']
    client_credentials_manager = spotipy.oauth2.SpotifyClientCredentials(spotify_client, spotify_secret)
    spotify = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

    all_features, data_features = autoencoder_data()

    song_count = data_features.shape[0]


    print(f"\nLoading album art for {song_count} songs...")
    album_art = []

    if os.path.exists(IMAGE_DIR) and os.path.isdir(IMAGE_DIR) and len(os.listdir(IMAGE_DIR)) == song_count:
        print("Album art already downloaded. Loading from files...")
        with alive_progress.alive_bar(song_count) as bar:
            for i in range(song_count):
                img = cv2.imread(f"{IMAGE_DIR}/{i}.jpg")
                album_art.append(img)
                bar()

        all_features = all_features[:song_count]
        album_art = np.asarray(album_art)
        data_features = data_features[:song_count]
        return all_features, album_art, data_features
    else:
        if not os.path.exists(IMAGE_DIR):
            os.makedirs(IMAGE_DIR)
        for file in os.listdir(IMAGE_DIR):
            os.remove(f"{IMAGE_DIR}/{file}")


        def download_album_art(i_and_url):
            i, url = i_and_url.split('-')
            i = int(i)

            req = urllib.request.urlopen(url)
            arr = np.asarray(bytearray(req.read()), dtype=np.uint8)
            img = cv2.imdecode(arr, -1)
            img = cv2.resize(img, IMAGE_SIZE)
            cv2.imwrite(f"{IMAGE_DIR}/{i}.jpg", img)
            return (i, img)

        
        print("Fetching art urls...")
        i_and_urls = []
        with alive_progress.alive_bar(song_count) as bar:
            for i in range(song_count):
                id = all_features.iloc[i]['id']
                track = spotify.track(id)
                url = track['album']['images'][0]['url']
                i_and_urls.append(f"{i}-{url}")
                bar()

        with multiprocessing.Pool(processes=8) as pool:
            print("Downloading album art...")
            # TODO: imap_unordered + sort + map vs just imap
            album_art = list(tqdm.tqdm(pool.imap_unordered(download_album_art, i_and_urls, CHUNK_SIZE), total=song_count))
            print("Sorting album art...")
            album_art.sort(key=lambda x: x[0])
            album_art = pool.map(lambda x: x[1], album_art)

        # print("Downloading album art...")
        # with alive_progress.alive_bar(song_count) as bar:
        #     for i in range(song_count):
        #         id = all_features.iloc[i]['id']
        #         track = spotify.track(id)
        #         url = track['album']['images'][0]['url']
        #         req = urllib.request.urlopen(url)
        #         arr = np.asarray(bytearray(req.read()), dtype=np.uint8)
        #         img = cv2.imdecode(arr, -1)
        #         img = cv2.resize(img, IMAGE_SIZE)
        #         cv2.imwrite(f"{IMAGE_DIR}/{i}.jpg", img)
        #         album_art.append(img)
        #         bar()

        return all_features, album_art, data_features
# ---------------------------------------------------------------------------- #