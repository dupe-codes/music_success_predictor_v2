"""
Implements a simple baseline algorithm for predicting
hotttnesss of songs.
"""

from sklearn import linear_model
import numpy as np

import config.settings as settings
from util.metadata import MetadataUtil
from util.analysis import AnalysisUtil

def train_model(linear_reg, train_set, artist_mapping, num_artists):
    """ Trains the linear regression model on simply artist indicator vars """
    inputs = [MetadataUtil.prepare_artist_feature_vec(data, artist_mapping, num_artists) for data in train_set]
    outputs = [data[settings.HOTTTNESSS_INDEX] for data in train_set]
    linear_reg.fit(np.array(inputs), np.array(outputs))

def test_model(linear_reg, test_set, artist_mapping, num_artists):
    """ Tests the linear regression model """
    inputs = [MetadataUtil.prepare_artist_feature_vec(data, artist_mapping, num_artists) for data in test_set]
    expected = [data[settings.HOTTTNESSS_INDEX] for data in test_set]

    results = linear_reg.predict(np.array(inputs))
    return results, expected


def run_baseline():
    """ Runs a simple linear regression model for prediction """
    util = MetadataUtil()
    training_set, testing_set = util.get_datasets()
    artist_mapping, num_artists = util.get_artist_features_info()

    linear_reg = linear_model.LinearRegression()
    train_model(linear_reg, training_set, artist_mapping, num_artists)
    predicted, expected = test_model(linear_reg, testing_set, artist_mapping, num_artists)

    analysis = AnalysisUtil(predicted, expected)
    accuracy = AnalysisUtil.percentage_accurracy()
    print 'Baseline predictor achieved accuracy of {}%'.format(accuracy)

    util.__teardown__()

if __name__ == '__main__':
    run_baseline()
