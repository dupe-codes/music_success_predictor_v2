"""
Makes API calls to echonest to get song data
"""

import sys
sys.path.append('./config/')

import requests
import settings
import time

def get_artist_genre(artist_name):
    """ Gets best genre to describe the given artist """
    data = {
        'api_key': settings.API_KEY,
        'name': artist_name,
        'format': 'json',
    }
    try:
        response = requests.get(settings.GENRE_API_ENDPOINT, params=data).json()
        data = response['response']['terms']
        return process_data(data)
    except:
        # API may be rate limiting, wait 60 seconds then try again...
        print 'Sleeping!'
        time.sleep(60)
        print 'Awake!'
        try:
            response = requests.get(settings.GENRE_API_ENDPOINT, params=data).json()
            data = response['response']['terms']
            return process_data(data)
        except:
            # If we fail again, just give up
            return None
    return None

def process_data(data):
    best_genre = None
    best_freq = 0
    for genre in data:
        if genre['frequency'] > best_freq:
            best_genre = genre['name']
            best_freq = genre['frequency']
    return best_genre
