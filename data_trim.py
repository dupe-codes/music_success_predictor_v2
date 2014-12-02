"""
Script to trim data down to a usable set for
learning.
"""

import sqlite3
import requests
import time

import config.settings as settings
from types import UnicodeType
from pyechonest import config
from pyechonest import song as SongAPI
config.ECHO_NEST_API_KEY = settings.API_KEY

def load_songs_with_lyrics(lyrics_db):
    query = ' '.join(['SELECT DISTINCT track_id FROM', settings.LYRICS_TABLE])
    response = lyrics_db.execute(query)
    songs = response.fetchall()
    return songs

def get_song_hotttnesss(song_name, artist_name):

    try:
        song_results = SongAPI.search(artist=artist_name, title=song_name)
    except:
        # Rate limited, gotta wait
        print 'Sleeping....'
        time.sleep(60)
        print 'Awake!'
        song_results = SongAPI.search(artist=artist_name, title=song_name)

    if not song_results: return None # Catch in scope above to see that no result found
    song_info = song_results[0]

    try:
        song_hotttnesss = song_info.get_song_hotttnesss()
    except:
        print 'Sleeping'
        time.sleep(60)
        print 'Awake'
        song_hotttnesss = song_info.get_song_hotttnesss()

    return song_hotttnesss

def migrate_songs(metadata_db, possible_songs):
    query = ' '.join(['SELECT * FROM', settings.SONGDATA_TABLE])
    #query = ' '.join(['SELECT * FROM', settings.SONGDATA_TABLE, 'WHERE track_id=\'{}\''.format(str(possible_songs[0][0]))])
    response = metadata_db.execute(query)
    all_songs = response.fetchall()

    result_db = sqlite3.connect(settings.SONGS_DB)
    cursor = result_db.cursor()
    for song in all_songs:
        if (song[0],) in possible_songs:
            song_hotttnesss = get_song_hotttnesss(song[1], song[6])
            if not song_hotttnesss: continue
            song = song + (song_hotttnesss,)

            values = '('
            for index, value in enumerate(song):
                if isinstance(value, UnicodeType):
                    value = str(value.encode('utf-8'))
                    value = value.replace("'", "''")
                values += '\'' + str(value) + '\''
                if index != len(song) - 1:
                    values += ', '
            values += ')'

            query = ' '.join(['INSERT INTO', settings.OURDATA_TABLE, 'VALUES', values])
            print 'Insert Query: {query}'.format(query=query)
            response = cursor.execute(query)
            print 'Stuck song with id {id} and hotttnesss {hottness} into db'.format(
                id=song[0],
                hottness=song_hotttnesss
            )

    result_db.commit()
    result_db.disconnect()
    print 'done!'


def trim_data():
    """ Creates a new database with only usable songs """
    lyrics_db = sqlite3.connect(settings.LYRICS_DB)
    metadata_db = sqlite3.connect(settings.METADATA_DB)

    possible_songs = load_songs_with_lyrics(lyrics_db)
    migrate_songs(metadata_db, possible_songs)

    lyrics_db.disconnect()
    metadata_db.disconnect()

if __name__ == '__main__':
    trim_data()
