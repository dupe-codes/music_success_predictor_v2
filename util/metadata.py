"""
Utility class to query the database for
song metadata
"""

# Janky way to get settings in python path
import sys
sys.path.append('./config/')

import settings
import json
import sqlite3

class MetadataUtil(object):
    """ Queries for song metadata """

    def __init__(self, use_json=False):
        self.use_json = use_json
        if not self.use_json:
            self.db = sqlite3.connect(settings.SONGS_DB)

    def __teardown__(self):
        """ Cleanup function """
        if not self.use_json:
            self.db.close()

    def get_artist_feature_info(self):
        """
        Returns info for creating artist indicator features 

        Returns a tuple of ({artist_name: index}, number of artists)
        """
        if not self.use_json:
            query = ' '.join(['SELECT DISTINCT artist_name FROM', settings.OURDATA_TABLE])
            response = self.db.execute(query)
            artists = response.fetchall()

            artist_mapping = {artist: index for index, artist in enumerate(artists)}
            return artist_mapping, len(artists)
        else:
            song_data = self._load_json_data()
            songs = song_data['song_data']
            partition_point = int(len(songs)*settings.PERCENT_TRAIN)
            songs = songs[:partition_point]

            artist_mapping = {}
            index = 0
            for song in songs:
                artist = song[1]['artist']
                if artist in artist_mapping: continue
                artist_mapping[artist] = index
                index += 1
            return artist_mapping, len(artist_mapping)

    def get_datasets(self):
        """ Returns sets to be used as training and testing sets """
        if not self.use_json:
            query = ' '.join(['SELECT * FROM', settings.OURDATA_TABLE])
            response = self.db.execute(query)
            songs = response.fetchall()
        else:
            song_data = self._load_json_data()
            songs = song_data['song_data']

        partition_point = int(len(songs)*settings.PERCENT_TRAIN)
        train_data = songs[:partition_point]
        test_data = songs[partition_point+1:]
        return  train_data, test_data

    def get_artist_lifespan(self, artist_name=None, artist_id=None):
        """ Gets the lifespan of a given artist """
        query = ' '.join(['SELECT year FROM', settings.OURDATA_TABLE, 'WHERE artist_name={}'.format(artist_name)])
        response = self.db.execute(query)
        results = response.fetchall()
        results = [x[0] for x in results if x[0] != 0]

        min_year = min(results)
        max_year = max(results)
        return max_year - min_year

    def _load_json_data(self):
        """ Returns song data loaded from the json file """
        with open(settings.JSON_DATA_PATH, 'r') as data:
            return json.load(data)

    @classmethod
    def prepare_artist_feature_vec(cls, data, artist_mapping, num_artists, use_json=False):
        feature_vector = [0]*num_artists
        if not use_json:
            artist_name = data[settings.ARTIST_NAME_INDEX]
            if artist_name in artist_mapping:
                feature_vector[artist_mapping[artist_name]] = 1
        else:
            artist_name = data[1]['artist']
            if artist_name in artist_mapping:
                feature_vector[artist_mapping[artist_name]] = 1

        return feature_vector
