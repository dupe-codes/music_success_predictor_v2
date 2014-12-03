"""
Utility class to query the database for
song metadata
"""

# Janky way to get settings in python path
import sys
sys.path.append('./config/')

import settings
import sqlite3

class MetadataUtil(object):
    """ Queries for song metadata """

    def __init__(self):
        self.db = sqlite3.connect(settings.SONGS_DB)
        pass

    def __teardown__(self):
        """ Cleanup function """
        self.db.close()

    def get_artist_feature_info(self):
        """
        Returns info for creating artist indicator features 

        Returns a tuple of ({artist_name: index}, number of artists)
        """
        query = ' '.join(['SELECT DISTINCT artist_name FROM', settings.OURDATA_TABLE])
        response = self.db.execute(query)
        artists = response.fetchall()

        artist_mapping = {artist: index for index, artist in enumerate(artists)}
        return artist_mapping, len(artists)

    def get_datasets(self):
        """ Returns sets to be used as training and testing sets """
        query = ' '.join(['SELECT * FROM', settings.OURDATA_TABLE])
        response = self.db.execute(query)
        songs = response.fetchall()

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

    @classmethod
    def prepare_artist_feature_vec(cls, data, artist_mapping, num_artists):
        feature_vector = [0]*num_artists
        artist_name = data[settings.ARTIST_NAME_INDEX]
        if artist_name in artist_mapping:
            feature_vector[artist_mapping[artist_name]] = 1

        return feature_vector
