import spotipy
import spotipy.oauth2
import dotenv



def create_sp():
    env = dotenv.dotenv_values('.env')
    spotify_client = env['SPOTIPY_CLIENT']
    spotify_secret = env['SPOTIPY_SECRET']
    client_credentials_manager = spotipy.oauth2.SpotifyClientCredentials(spotify_client, spotify_secret)
    sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

    return sp

# def search_spotify(sp, query):
#     result = sp.search(q=query, limit=15, type='track')
#     items = result['tracks']['items']
#     return items

# def fetch_track(sp, track_id):
#     result = sp.track(track_id)
#     return result