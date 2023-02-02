import collections
import os

import spotipy
from loguru import logger
from quarter_lib.config import get_secrets
from spotipy.oauth2 import SpotifyOAuth

CLIENT_ID, CLIENT_SECRET = get_secrets(
    ['spotify/client_id', 'spotify/client_secret'])

logger.add(
    os.path.join(os.path.dirname(os.path.abspath(__file__)) + "/logs/" + os.path.basename(__file__) + ".log"),
    format="{time:YYYY-MM-DD at HH:mm:ss} | {level} | {message}",
    backtrace=True,
    diagnose=True,
)

REDIRECT_URI = ("http://localhost:4466",)
SCOPE = ["playlist-read-private", "user-read-recently-played", "user-top-read"]
SPOTIFY_API = spotipy.Spotify(
    auth_manager=SpotifyOAuth(
        client_id=CLIENT_ID,
        client_secret=CLIENT_SECRET,
        redirect_uri=REDIRECT_URI,
        scope=SCOPE,
    )
)


def get_recently_played(cursors=None):
    recently_played = (
        SPOTIFY_API.current_user_recently_played(limit=50, after=cursors["after"])  # Before or after?!
        if cursors
        else SPOTIFY_API.current_user_recently_played(limit=50)
    )
    logger.info("{len_items} songs grabbed".format(len_items=len(recently_played["items"])))
    new_list = [flatten(item) for item in recently_played["items"]]
    return new_list, recently_played["cursors"]


def flatten(d, parent_key="", sep="_"):
    items = []
    for k, v in d.items():
        if "available_markets" not in k:
            new_key = parent_key + sep + k if parent_key else k
            if isinstance(v, collections.MutableMapping):
                items.extend(flatten(v, new_key, sep=sep).items())
            else:
                items.append((new_key, v))
    return dict(items)
