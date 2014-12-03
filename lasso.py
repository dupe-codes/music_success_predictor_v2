"""
Implements linear regression with L1 penalty
"""

from sklearn.linear_model import Lasso
#from sklearn.linear_model import LinearRegression as Lasso

import numpy as np

import config.settings as settings
from util.metadata import MetadataUtil
from util.analysis import AnalysisUtil


def train_model(lasso_model, training_set, util):
    # Grab info for artist indicator features
    artist_mapping, num_artists = util.get_artist_feature_info()

    # First prepare input feature vectors
    inputs = []
    for data in training_set:
        feature_vector = MetadataUtil.prepare_artist_feature_vec(data, artist_mapping, num_artists, use_json=True)
        feature_vector += MetadataUtil.prepare_metadata_features(data, use_json=True)
        inputs.append(feature_vector)
    outputs = [data[2] for data in training_set]

    lasso_model.fit(np.array(inputs), np.array(outputs))

def test_model(lasso_model, testing_data, util):
    artist_mapping, num_artists = util.get_artist_feature_info()

    inputs = []
    for data in testing_data:
        feature_vector = MetadataUtil.prepare_artist_feature_vec(data, artist_mapping, num_artists, use_json=True)
        feature_vector += MetadataUtil.prepare_metadata_features(data, use_json=True)
        inputs.append(feature_vector)
    expected = [data[2] for data in testing_data]

    results = lasso_model.predict(np.array(inputs))
    rsquared_score = lasso_model.score(np.array(inputs), np.array(expected))
    return results, expected, rsquared_score

def run_basic_features():
    """ Runs a lasso regression model on basic metadata features """

    print 'Preparing data with basic features...'
    util = MetadataUtil(use_json=True)
    training_set, testing_set = util.get_datasets()

    print 'Training lasso model...'
    #lasso_model = Lasso(alpha=0.1)
    lasso_model = Lasso()
    train_model(lasso_model, training_set, util)

    print 'Testing lasso model...'
    predicted, expected, rsquared = test_model(lasso_model, testing_set, util)

    analysis = AnalysisUtil(predicted, expected)
    accuracy = analysis.percentage_accuracy()
    print 'Lasso predictor with basic features achieved accuracy of {}%'.format(accuracy)
    print 'R^2 score calculated by sklearn: {}'.format(rsquared)

    print 'Done'
    util.__teardown__()

if __name__ == '__main__':
    run_basic_features()
