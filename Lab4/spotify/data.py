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

# import bing_image_downloader
from bing_image_downloader import downloader

import tensorflow as tf
import tensorflow.data as data
BUFFER_SIZE = 2000
BATCH_SIZE = 64
PREFETCH_SIZE = 2

# import tqdm
# import multiprocessing
# CHUNK_SIZE = 100

import math
MAX_TRACKS = 50

BAR_GROUPS = 6

IMAGE_SIZE = (128, 128)

BASE_DIR  = 'output/save-cnn'
IMAGE_DIR = 'output/save-cnn/images'
BING_IMAGE_DIR = 'output/save-cnn/bing_images'
BING_TEMP_DIR = 'output/save-cnn/bing_temp'
URL_FILE  = 'output/save-cnn/urls.txt'


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
    if not os.path.exists(IMAGE_DIR):
        os.makedirs(IMAGE_DIR)

    print("Downloading album art...")
    with alive_progress.alive_bar(song_count) as bar:
        for i_and_url in i_and_urls:
            download_album_art(i_and_url)
            bar()

    # with multiprocessing.Pool(processes=8) as pool:
    #     album_art = list(tqdm.tqdm(pool.imap_unordered(download_album_art, i_and_urls, CHUNK_SIZE), total=song_count))
    #     print("Sorting album art...")
    #     album_art.sort(key=lambda x: x[0])
    #     album_art = pool.map(lambda x: x[1], album_art)

def download_album_art(i_and_url):
    i, url = i_and_url
    url = url.strip()

    try:
        req = urllib.request.urlopen(url)
        arr = np.asarray(bytearray(req.read()), dtype=np.uint8)
        img = cv2.imdecode(arr, -1)
        img = cv2.resize(img, IMAGE_SIZE)
    except (urllib.error.HTTPError, cv2.error, ValueError) as e:
        print(f"{e}: Error downloading image {i} from {url}. Using random image.")
        img = np.random.randint(0, 256, (IMAGE_SIZE[0], IMAGE_SIZE[1], 3), dtype=np.uint8)        
        
    # pad with name with zeros to preserve lexicographical order
    file_name = f"{IMAGE_DIR}/{i:06}.jpg"
    cv2.imwrite(file_name, img)

def load_art_from_files(song_count, folder):
    print("Trying to load album art from files...")

    if os.path.exists(folder) and os.path.isdir(folder) and len(os.listdir(folder)) == song_count:
        print("Loading from files...")

        def load_file(x):
            return tf.constant(np.array(PIL.Image.open(x.numpy()).convert("RGB")))
       
        images_ds = data.Dataset.list_files(f"{folder}/*.jpg")
        images_ds = images_ds.map(lambda x: tf.py_function(load_file, [x], [tf.uint8]))
        return images_ds

        # album_art = []
        # with alive_progress.alive_bar(song_count) as bar:
        #     for i in range(song_count):
        #         img = cv2.imread(f"{dir}/{i:06}.jpg")
        #         album_art.append(img)
        #         bar()
        # return album_art
    else:
        print("Album art not found or does not match song count. Fetching...")
        return None
    
def download_all_from_bing(all_features, song_count):
    print("Downloading art from Bing...")

    if not os.path.exists(BING_IMAGE_DIR):
        os.makedirs(BING_IMAGE_DIR)
    if not os.path.exists(BING_TEMP_DIR):
        os.makedirs(BING_TEMP_DIR)

    with alive_progress.alive_bar(song_count) as bar:
        for i, feature in all_features.iterrows():
            load_art_from_bing(feature, i)
            bar()

def load_art_from_bing(feature, i):
    artists_list = feature['artists'].replace('[', '').replace(']', '').replace("'", '').split(', ')
    query = f"{feature['name']} {' '.join(artists_list)}"
    downloader.download(
        query,
        limit=2,
        output_dir=BING_TEMP_DIR,
        adult_filter_off=False,
        filter='photo',
        force_replace=True,
        timeout=10,
        verbose=False,
    )

    folder_path = f"{BING_TEMP_DIR}/{query}"
    files_in_dir = os.listdir(folder_path)

    imgs = []
    for file in files_in_dir:
        img = cv2.imread(f"{folder_path}/{file}")
        imgs.append(img)
        os.remove(f"{folder_path}/{file}")
    
    valid_img = None
    for img in imgs:
        try:
            img = cv2.resize(img, IMAGE_SIZE)
            valid_img = img
            break
        except cv2.error: pass

    if valid_img is None:
        print(f"No art: '{query}'. Using random image.")
        img = np.random.randint(0, 256, (IMAGE_SIZE[0], IMAGE_SIZE[1], 3), dtype=np.uint8)

    os.rmdir(folder_path)

    file_name = f"{BING_IMAGE_DIR}/{i:06}.jpg"
    cv2.imwrite(file_name, img)


def cnn_data():
    all_features, data_features = autoencoder_data()
    song_count = data_features.shape[0]

    print(f"\nLoading album art for {song_count} songs...")

    # images_ds = load_art_from_files(song_count, IMAGE_DIR)
    # if images_ds is None:
    #     i_and_urls = get_urls(all_features, song_count)
    #     download_all_album_art(i_and_urls, song_count)
    #     images_ds = load_art_from_files(song_count, IMAGE_DIR)

    images_ds = load_art_from_files(song_count, BING_IMAGE_DIR)
    if images_ds is None:
        download_all_from_bing(all_features, song_count)
        images_ds = load_art_from_files(song_count, BING_IMAGE_DIR)
        
    data_labels = data.Dataset.from_tensor_slices(data_features)
    train_ds = (data.Dataset.zip((images_ds, data_labels))
        .shuffle(BUFFER_SIZE, reshuffle_each_iteration=True)
        .batch(BATCH_SIZE)
        .prefetch(PREFETCH_SIZE))
    
    print(train_ds)

    images = (img[0].numpy()for img in images_ds)
    
    return all_features, train_ds, images
# ---------------------------------------------------------------------------- #