"""
We gonna plot some data
"""

import config.settings as settings
from util.metadata import MetadataUtil

import numpy as np
import plotly.plotly as py
from plotly.graph_objs import *

py.sign_in('Python-Demo-Account', 'gwt101uhh0')


if __name__ == '__main__':

    util = MetadataUtil({})
    hotttnesss = util.get_hotttnesss_scores()

    data = Data([
        Histogram(
            x=hotttnesss
        )
    ])
    plot_url = py.plot(data, filename='hotttnesss-histogram')
    print 'Plot can now be found at: ' + str(plot_url)
