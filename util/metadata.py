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

settings.FILTER = 'WHERE song_hotttnesss > 0 and year > 0 and artist_hotttnesss > 0'

class MetadataUtil(object):
    """ Queries for song metadata """

    def __init__(self, features, use_json=False):
        self.features = features
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
            query = ' '.join(['SELECT * FROM', settings.OURDATA_TABLE, settings.FILTER])
            response = self.db.execute(query)
            songs = response.fetchall()
        else:
            song_data = self._load_json_data()
            songs = song_data['song_data']

        partition_point = int(len(songs)*settings.PERCENT_TRAIN)
        train_data = songs[:partition_point]
        test_data = songs[partition_point+1:]
        return  train_data, test_data

    def get_hotttnesss_scores(self):
        if not self.use_json:
            query = ' '.join(['SELECT song_hotttnesss FROM', settings.OURDATA_TABLE, settings.FILTER])
            response = self.db.execute(query)
            hotttnesss = response.fetchall()
            hotttnesss = [value[0] for value in hotttnesss]
        return hotttnesss

    def get_artist_hotttnesss_scores(self):
        if not self.use_json:
            query = ' '.join(['SELECT artist_hotttnesss FROM', settings.OURDATA_TABLE, settings.FILTER])
            response = self.db.execute(query)
            hotttnesss = response.fetchall()
            hotttnesss = [value[0] for value in hotttnesss]
        return hotttnesss

    def get_artist_lifespan(self, artist_name=None, artist_id=None):
        """ Gets the lifespan of a given artist """
        if not self.use_json:
            artist_name = artist_name.replace("'", "''").encode('utf-8')
            query = ' '.join(['SELECT year FROM', settings.OURDATA_TABLE, 'WHERE artist_name=\'{}\''.format(artist_name)])
            response = self.db.execute(query)
            results = response.fetchall()
            results = [x[0] for x in results if x[0] != 0]

            if not results: return 0
            min_year = min(results)
            max_year = max(results)
            return max_year - min_year
        else:
            return 0 # Oops, we aren't saving the year in the json data...
            song_data = self._load_json_data()['song_data']
            for song in song_data:
                song_artist = song[1]['artist']
                if artist_name == song_artist: pass

    def get_num_popular_songs(self, artist_name=None):
        """ Returns number of popular songs for the given artist """
        if not self.use_json:
            artist_name = artist_name.replace("'", "''").encode('utf-8')
            query = ' '.join([
                'SELECT song_hotttnesss FROM',
                settings.OURDATA_TABLE,
                'WHERE artist_name=\'{}\''.format(artist_name),
                'AND',
                'song_hotttnesss > {}'.format(settings.POPULAR_SONG_THRESHOLD)
            ])
            response = self.db.execute(query)
            results = response.fetchall()
            return len(results)
        else:
            song_data = self._load_json_data()['song_data']
            num_popular = 0
            for song in song_data:
                if song[1]['artist'] == artist_name:
                    song_hotttnesss = song[2]
                    if song_hotttnesss >= settings.POPULAR_SONG_THRESHOLD:
                        num_popular += 1
            return num_popular

    def get_genre_statistics(self):
        query = ' '.join(['SELECT genre, song_hotttnesss FROM', settings.OURDATA_TABLE, settings.FILTER])
        response = self.db.execute(query)
        genres = response.fetchall()

        query = ' '.join(['SELECT genre, count(genre) AS test_value FROM', settings.OURDATA_TABLE, 'GROUP BY genre ORDER BY test_value'])
        response = self.db.execute(query)
        genre_counts = response.fetchall()

        cutoff = 40
        valid_genres = [value[0] for value in genre_counts if value[1] >= cutoff]

        genre_stats = {}
        for genre_name, song_hotttnesss in genres:
            if genre_name not in valid_genres: continue
            # AHHHH WHY
            if genre_name in genre_stats:
                stats = genre_stats[genre_name]
                if song_hotttnesss >= settings.POPULAR_SONG_THRESHOLD:
                    stats['popular'] += 1
                else:
                    stats['unpopular'] += 1
                genre_stats[genre_name] = stats
            else:
                if song_hotttnesss >= settings.POPULAR_SONG_THRESHOLD:
                    stats = { 'popular': 1, 'unpopular': 0 }
                else:
                    stats = { 'popular': 0, 'unpopular': 1 }
                genre_stats[genre_name] = stats

        return genre_stats

    def get_genre_feature_info(self):
        if self.use_json:
            return None, 0
        else:
            query = ' '.join(['SELECT genre FROM', settings.OURDATA_TABLE])
            response = self.db.execute(query)
            genres = response.fetchall()

            genre_mapping = {}
            index = 0
            for genre in genres:
                genre_name = genre[0]
                if genre_name in genre_mapping: continue
                genre_mapping[genre_name] = index
                index += 1
            return genre_mapping, len(genre_mapping)

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

    @classmethod
    def prepare_metadata_features(cls, data, features, use_json=False):
        result = []
        if use_json:
            feature_dict = data[1]
            for feature, value in feature_dict.iteritems():
                if feature != 'artist' and feature != 'genre':
                    if value is None: value = 0
                    result.append(value)
        else:
            for index in settings.FEATURE_INDICES:
                if features[index]:
                    result.append(data[index])

        return result

    @classmethod
    def prepare_genre_feature_vec(cls, data, genre_mapping, num_genres, use_json=False):
        genre_vector = [0]*num_genres
        if not use_json:
            genre = data[settings.GENRE_INDEX]
            if genre in genre_mapping:
                genre_vector[genre_mapping[genre]] = 1
        else:
            pass
        return genre_vector
