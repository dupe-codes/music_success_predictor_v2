"""
Implements K nearest neighbors
"""

from sklearn.neighbors import KNeighborsRegressor
import numpy as np

import config.settings as settings
from util.metadata import MetadataUtil
from util.analysis import AnalysisUtil

settings.USE_ARTIST_LIFESPAN = False

def train_model(neighbors_model, training_set, util):
    # Grab info for artist indicator features
    artist_mapping, num_artists = util.get_artist_feature_info()

    # First prepare input feature vectors
    inputs = []
    for data in training_set:
        feature_vector = MetadataUtil.prepare_artist_feature_vec(data, artist_mapping, num_artists, use_json=util.use_json)
        feature_vector += MetadataUtil.prepare_metadata_features(data, use_json=util.use_json)
        if settings.USE_ARTIST_LIFESPAN:
            feature_vector.append(util.get_artist_lifespan(artist_name=data[settings.ARTIST_NAME_INDEX]))
        inputs.append(feature_vector)

    if util.use_json:
        outputs = [data[2] for data in training_set]
    else:
        outputs = [data[settings.HOTTTNESSS_INDEX] for data in training_set]

    neighbors_model.fit(np.array(inputs), np.array(outputs))

def test_model(neighbors_model, testing_data, util):
    artist_mapping, num_artists = util.get_artist_feature_info()

    inputs = []
    for data in testing_data:
        feature_vector = MetadataUtil.prepare_artist_feature_vec(data, artist_mapping, num_artists, use_json=util.use_json)
        feature_vector += MetadataUtil.prepare_metadata_features(data, use_json=util.use_json)
        if settings.USE_ARTIST_LIFESPAN:
            feature_vector.append(util.get_artist_lifespan(artist_name=data[settings.ARTIST_NAME_INDEX]))

        inputs.append(feature_vector)

    if util.use_json:
        expected = [data[2] for data in testing_data]
    else:
        expected = [data[settings.HOTTTNESSS_INDEX] for data in testing_data]

    results = neighbors_model.predict(np.array(inputs))
    rsquared_score = neighbors_model.score(np.array(inputs), np.array(expected))
    return results, expected, rsquared_score

def run_basic_features():
    """ Runs a k nearest neighbors model on basic metadata features """

    print 'Preparing data with basic features...'
    util = MetadataUtil(use_json=True)
    training_set, testing_set = util.get_datasets()

    print 'Training neighbors model...'
    neighbors_model = KNeighborsRegressor(n_neighbors=settings.NUM_NEIGHBORS)
    train_model(neighbors_model, training_set, util)

    print 'Testing neighbors model...'
    predicted, expected, rsquared = test_model(neighbors_model, testing_set, util)

    analysis = AnalysisUtil(predicted, expected)
    accuracy = analysis.percentage_accuracy()
    print 'Neighbors predictor with basic features achieved accuracy of {}%'.format(accuracy)
    print 'R^2 score calculated by sklearn: {}'.format(rsquared)

    print 'Done'
    util.__teardown__()

def run_features_with_lifespans():
    """ Runs a k nearest neighbors model with features including artist lifespan """

    print 'Preparing data with artist lifespan feature...'
    util = MetadataUtil(use_json=False)
    training_set, testing_set = util.get_datasets()

    print 'Training k nearest neighbors model...'
    neighbors_model = KNeighborsRegressor(n_neighbors=settings.NUM_NEIGHBORS)
    train_model(neighbors_model, training_set, util)

    print 'Testing neighbors model...'
    predicted, expected, rsquared = test_model(neighbors_model, testing_set, util)

    analysis = AnalysisUtil(predicted, expected)
    accuracy = analysis.percentage_accuracy()
    print 'neighbors predictor with basic features achieved accuracy of {}%'.format(accuracy)
    print 'R^2 score calculated by sklearn: {}'.format(rsquared)

    print 'Done'
    util.__teardown__()

if __name__ == '__main__':
    run_basic_features()

    settings.USE_ARTIST_LIFESPAN = True
    run_features_with_lifespans()
