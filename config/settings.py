"""
Project settings
"""

METADATA_DB = 'data/track_metadata.db'
LYRICS_DB = 'data/mxm_dataset.db'
SONGS_DB = 'data/usable_songs.db'

LYRICS_TABLE = 'lyrics'
SONGDATA_TABLE = 'songs'
OURDATA_TABLE = 'good_songs'

JSON_DATA_PATH = 'data/json/song_data.json'

API_KEY = '0AUAGZNQLKRLAILXK'

ARTIST_NAME_INDEX = 6
HOTTTNESSS_INDEX = 14

FEATURE_INDICIES = [
    1,
]

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
