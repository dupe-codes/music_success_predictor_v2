"""
Implements linear regression with L1 penalty
"""

from sklearn.linear_model import Lasso
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

def run_basic_features():
    """ Runs a lasso regression model on basic metadata features """

    print 'Preparing data...'
    util = MetadataUtil(use_json=True)
    training_set, testing_set = util.get_datasets()

    print 'Training lasso model...'
    lasso_model = Lasso(alpha=0.1)
    train_model(lasso_model, training_set, util)

    util.__teardown__()

if __name__ == '__main__':
    run_basic_features()
