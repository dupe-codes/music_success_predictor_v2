"""
Implements a simple baseline algorithm for predicting
hotttnesss of songs.
"""

from sklearn import linear_model
import numpy as np

import config.settings as settings
from util.metadata import MetadataUtil
from util.analysis import AnalysisUtil


def train_model(linear_reg, train_set, artist_mapping, num_artists, get_train_error=False):
    """ Trains the linear regression model on simply artist indicator vars """
    inputs = [MetadataUtil.prepare_artist_feature_vec(data, artist_mapping, num_artists, use_json=False) for data in train_set]
    outputs = [data[settings.HOTTTNESSS_INDEX] for data in train_set]
    #outputs = [song[2] for song in train_set]
    linear_reg.fit(np.array(inputs), np.array(outputs))

    # Run on training data to get training error
    results = None
    expected = None
    rsquared_score = None
    if get_train_error:
        results = linear_reg.predict(np.array(inputs))
        rsquared_score = linear_reg.score(np.array(inputs), np.array(outputs))
        expected = outputs
    return results, expected, rsquared_score

def test_model(linear_reg, test_set, artist_mapping, num_artists):
    """ Tests the linear regression model """
    inputs = [MetadataUtil.prepare_artist_feature_vec(data, artist_mapping, num_artists, use_json=False) for data in test_set]
    expected = [data[settings.HOTTTNESSS_INDEX] for data in test_set]
    #expected = [song[2] for song in test_set]

    results = linear_reg.predict(np.array(inputs))
    rsquared_score = linear_reg.score(np.array(inputs), np.array(expected))
    return results, expected, rsquared_score


def run_baseline():
    """ Runs a simple linear regression model for prediction """

    print 'Preparing data...'
    util = MetadataUtil({}, use_json=False)
    training_set, testing_set = util.get_datasets()
    artist_mapping, num_artists = util.get_artist_feature_info()

    print 'Training linear model...'
    linear_reg = linear_model.LinearRegression()
    train_predicted, train_expected, train_rscore = train_model(linear_reg, training_set, artist_mapping, num_artists, get_train_error=True)

    analysis = AnalysisUtil(train_predicted, train_expected)
    accuracy = analysis.percentage_accuracy()
    print '\nPredictor achieved a training error of {}'.format(accuracy)
    print '\nR^2 score calculated by sklearn: {}'.format(train_rscore)

    print '\nTesting linear model...'
    predicted, expected, rsquared = test_model(linear_reg, testing_set, artist_mapping, num_artists)

    analysis = AnalysisUtil(predicted, expected)
    accuracy = analysis.percentage_accuracy()
    print 'Baseline predictor achieved accuracy of {}%'.format(accuracy)
    print 'R^2 score calculated by sklearn: {}'.format(rsquared)

    util.__teardown__()

if __name__ == '__main__':
    run_baseline()
