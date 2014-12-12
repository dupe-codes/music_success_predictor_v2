"""
Project settings
"""

METADATA_DB = 'data/track_metadata.db'
LYRICS_DB = 'data/mxm_dataset.db'
SONGS_DB = 'data/usable_songs.db'

LYRICS_TABLE = 'lyrics'
SONGDATA_TABLE = 'songs'
OURDATA_TABLE = 'good_songs_v2'

JSON_DATA_PATH = 'data/json/song_data.json'

API_KEY = '0AUAGZNQLKRLAILXK'

ARTIST_NAME_INDEX = 6
HOTTTNESSS_INDEX = 14

FEATURE_INDICES = [
    7,
    8,
    9,
    10,
    15,
    16,
    17,
    18,
    19,
    20,
]

DURATION = 7
ARTIST_FAMILIARITY = 8
ARTIST_HOTTTNESSS = 9
YEAR = 10
TEMPO = 15
DANCEABILITY = 16
ENERGY = 17
LOUDNESS = 18
KEY = 19
TIME_SIGNATURE = 20

SONG_FEATURES = [
    'tempo',
    'danceability',
    'energy',
    'loudness',
    'key',
    'duration',
    'time_signature',
    'speechiness',
    'liveness',
]

PERCENT_TRAIN = 0.70
PERCENT_TEST = 0.30

NUM_NEIGHBORS = 8
# Changing this led to slight changes

POPULAR_SONG_THRESHOLD = 0.6
# NOTE: Changing this doesn't seem to affect anything

GENRES = [
    'rap',
    'rock',
    'country',
    'hip hop',
    'indie rock',
    'pop',
    'r&b',
    'folk',
    'funk',
    'pop house',
    'pop rap',
    'power pop',
    'alternative hip hop',
    'alternative pop',
    'alternative r&b',
    'alternative rock',
    'broadway',
    'christmas',
    'classic rock',
    'country blues',
    'country rock',
    'deep alternative r&b',
    'hard rock',
    'indie pop',
    'jazz',
    'metal',
    'pop',
    'pop rock',
    'progressive metal',
]
