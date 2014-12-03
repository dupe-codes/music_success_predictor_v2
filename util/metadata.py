"""
Utility class to query the database for
song metadata
"""

# May have to do jankiness to get this imported
import ..config.settings as settings
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
        return {}, 0

    def prepare_artist_feature_vec(data, artist_mapping, num_artists):
        feature_vector = [0]*num_artists
        artist_name = data[settings.ARTIST_NAME_INDEX]
        if artist_name in artist_mapping:
            feature_vector[artist_mapping[artist_name]] = 1

        return feature_vector

    def get_datasets(self):
        """ Returns sets to be used as training and testing sets """
        return  set(), set()

    def get_artist_lifespan(self, artist_name=None, artist_id=None):
        """ Gets the lifespan of a given artist """
        query = ' '.join(['SELECT year FROM', settings.OURDATA_TABLE, 'WHERE artist_name={}'.format(artist_name)])
        response = self.db.execute(query)
        results = response.fetchall()
        results = [x[0] for x in results if x[0] != 0]

        min_year = min(results)
        max_year = max(results)
        return max_year - min_year
