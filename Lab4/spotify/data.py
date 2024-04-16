import alive_progress

import pandas as pd
import numpy as np

import PIL

import spotipy
import spotipy.oauth2
import urllib
import cv2
import os
import dotenv


import tensorflow as tf
import tensorflow.data as data
BUFFER_SIZE = 2000
BATCH_SIZE = 64
PREFETCH_SIZE = 2


import requests
import base64
from bs4 import BeautifulSoup

import math
MAX_TRACKS = 50

BAR_GROUPS = 6

IMAGE_SIZE = (128, 128)

BASE_DIR  = 'output/save-cnn/images'
ALBUM_DIR = 'output/save-cnn/images/album'
GOOGLE_DIR = 'output/save-cnn/images/google'
URL_FILE  = 'output/save-cnn/images/urls.txt'


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
# ---------------------------------------------------------------------------- #


# ---------------------------------------------------------------------------- #
def get_urls(all_features, song_count):
    print("Trying to load album art urls...")

    if os.path.exists(URL_FILE) and os.path.isfile(URL_FILE):
        print("URL file already exists. Loading...")
        with open(URL_FILE, 'r') as f:
            all_lines = f.readlines()
            
            if len(all_lines) == song_count:
                i_and_urls = enumerate(all_lines)
                return i_and_urls
            else:
                print(f"Expected {song_count} urls, found {len(all_lines)} urls. Fetching...")
    else:
        os.makedirs(BASE_DIR, exist_ok=True)
    
    env = dotenv.dotenv_values('.env')
    spotify_client = env['SPOTIPY_CLIENT']
    spotify_secret = env['SPOTIPY_SECRET']
    client_credentials_manager = spotipy.oauth2.SpotifyClientCredentials(spotify_client, spotify_secret)
    spotify = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

    print("Reading song ids...")
    ids = [all_features.iloc[i]['id'] for i in range(song_count)]

    print("Fetching art urls from Spotify...")
    i_and_urls = []
    track_chunk_count = math.ceil(song_count / MAX_TRACKS)
    with open(URL_FILE, 'w') as f:
        with alive_progress.alive_bar(track_chunk_count) as bar:
            for i in range(0, song_count, MAX_TRACKS):
                tracks = spotify.tracks(ids[i:i + MAX_TRACKS])
                
                for track in tracks['tracks']:
                    try:
                        url = track['album']['images'][0]['url']
                    except IndexError:
                        print(f"No album art for {track['name']} ({track['id']} {track['album']['id']}). Using random image.")
                        url = '????'
                    f.write(f"{url}\n")
                    i_and_urls.append((i, url))
                
                bar()

    return i_and_urls

def download_all_album_art(i_and_urls, song_count):
    if not os.path.exists(ALBUM_DIR):
        os.makedirs(ALBUM_DIR)

    print("Checking for existing album art files...")
    highest_existing_id = -1
    with alive_progress.alive_bar(song_count) as bar:
        for i in range(song_count):
            file_name = f"{ALBUM_DIR}/{i:06}.jpg"
            if os.path.exists(file_name):
                highest_existing_id = i
            else:
                break
            bar()
    
    if highest_existing_id > -1:
        print(f"Found {highest_existing_id + 1} existing album art files.")

    new_songs = song_count - highest_existing_id - 1
    print("Downloading album art...")
    with alive_progress.alive_bar(new_songs) as bar:
        for (i, url) in i_and_urls:
            file_name = f"{ALBUM_DIR}/{i:06}.jpg"
            if i > highest_existing_id and not os.path.exists(file_name):
                download_album_art(url, file_name)
            bar()

def download_album_art(url, file_name):
    url = url.strip()

    try:
        req = urllib.request.urlopen(url)
        arr = np.asarray(bytearray(req.read()), dtype=np.uint8)
        img = cv2.imdecode(arr, -1)
        img = cv2.resize(img, IMAGE_SIZE)
    except (urllib.error.HTTPError, cv2.error, ValueError) as e:
        print(f"{e}: Error downloading image {file_name} from {url}. Using random image.")
        img = np.random.randint(0, 256, (IMAGE_SIZE[0], IMAGE_SIZE[1], 3), dtype=np.uint8)        
        
    # pad with name with zeros to preserve lexicographical order
    cv2.imwrite(file_name, img)

def load_art_from_files(song_count, folder):
    print("Trying to load art from files...")

    if os.path.exists(folder) and os.path.isdir(folder) and len(os.listdir(folder)) == song_count:
        print("Loading from files...")

        def load_file(x):
            return tf.constant(np.array(PIL.Image.open(x.numpy()).convert("RGB")))
       
        images_ds = data.Dataset.list_files(f"{folder}/*.jpg")
        images_ds = images_ds.map(lambda x: tf.py_function(load_file, [x], [tf.uint8]))
        return images_ds
    else:
        print("Album art not found or does not match song count. Fetching...")
        return None

def download_all_google_art(all_features, song_count):
    if not os.path.exists(GOOGLE_DIR):
        os.makedirs(GOOGLE_DIR)

    print("Checking for existing google art files...")
    highest_existing_id = -1
    with alive_progress.alive_bar(song_count) as bar:
        for i in range(song_count):
            file_name = f"{GOOGLE_DIR}/{i:06}.jpg"
            if os.path.exists(file_name):
                highest_existing_id = i
            else:
                break
            bar()

    if highest_existing_id > -1:
        print(f"Found {highest_existing_id + 1} existing google art files.")

    new_songs = song_count - highest_existing_id - 1
    print("Downloading google art...")
    with alive_progress.alive_bar(new_songs) as bar:
        for i, feature in all_features.iterrows():
            file_name = f"{GOOGLE_DIR}/{i:06}.jpg"
            if i > highest_existing_id and not os.path.exists(file_name):
                download_google_art(feature['name'], feature['artists'], file_name)
                bar()

def try_get_google_art(search):
    url = f"https://www.google.com/search?hl=en&tbm=isch&q={search}"
    response = requests.get(url, headers={"User-Agent": "Mozilla/5.0"})

    if response.status_code != 200: return None

    soup = BeautifulSoup(response.text, 'html.parser')
    image_eles = soup.findAll('img')

    if not image_eles or len(image_eles) < 9: return None

    # 8: magic number which is usually the first image tag for the search results
    image_ele = image_eles[8]
    image_src = image_ele['src']

    if image_src.startswith("data:image"):
        encoded = image_src.split(',')[1]
        nparr = np.frombuffer(base64.b64decode(encoded), np.uint8)
        img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
        return img
    elif image_src.startswith("http"):
        img_response = requests.get(image_src)
        if img_response.status_code != 200: return None
        img = cv2.imdecode(np.frombuffer(img_response.content, np.uint8), cv2.IMREAD_COLOR)

    img = cv2.resize(img, IMAGE_SIZE)
    return img

def download_google_art(name, artists, file_name):
    artists_str = artists.replace('[', '').replace(']', '').replace("'", '').replace(", ", ' ')
    searches = [
        f"{name} {artists_str} yt",
        f"{name} {artists_str}",
        f"{name} yt",
        f"{name}",
        f"{artists_str}",
    ]

    img = None
    for search in searches:
        search = search.replace(' ', '+')
        img = try_get_google_art(search)
        if img is not None: break

    if img is None:
        print(f"Error downloading image {file_name} from google. Using random image.")
        img = np.random.randint(0, 256, (IMAGE_SIZE[0], IMAGE_SIZE[1], 3), dtype=np.uint8)

    cv2.imwrite(file_name, img)


def cnn_data(google_mode):
    all_features, data_features = autoencoder_data()
    song_count = data_features.shape[0]

    print(f"\nLoading album art for {song_count} songs...")

    if google_mode:
        images_ds = load_art_from_files(song_count, GOOGLE_DIR)
        if images_ds is None:
            download_all_google_art(all_features, song_count)
            images_ds = load_art_from_files(song_count, GOOGLE_DIR)
    else:
        images_ds = load_art_from_files(song_count, ALBUM_DIR)
        if images_ds is None:
            i_and_urls = get_urls(all_features, song_count)
            download_all_album_art(i_and_urls, song_count)
            images_ds = load_art_from_files(song_count, ALBUM_DIR)
        
    data_labels = data.Dataset.from_tensor_slices(data_features)
    train_ds = (data.Dataset.zip((images_ds, data_labels))
        .shuffle(BUFFER_SIZE, reshuffle_each_iteration=True)
        .batch(BATCH_SIZE)
        .prefetch(PREFETCH_SIZE))
    
    print(train_ds)

    # Note: generator is used to avoid loading all images into memory
    images = (img[0].numpy() for img in images_ds)
    
    return all_features, train_ds, images
# ---------------------------------------------------------------------------- #