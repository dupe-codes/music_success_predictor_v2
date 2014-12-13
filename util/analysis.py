"""
Defines an analysis class to analyze algorithm results
"""

import sys
sys.path.append('./config/')
import settings


class AnalysisUtil(object):

    def __init__(self, predicted, expected, threshold=0.30):
        """
        Initializes object to analyze given data

        Params: expected - dict of song title => actual scores
                predicted - dict of song title => predicted scores
        TODO: Disregard this comment, the params are lists
        """
        self.expected = expected
        self.predicted = predicted
        self.threshold = threshold

    def percentage_accuracy(self):
        """ Returns the ratio of accurately predicted scores """
        numCorrect = 0
        """
        for song, predicted in self.predicted.iteritems():
            expected_val = self.expected[song]
            if abs(predicted - expected_val) < self.threshold:
                numCorrect += 1
        """
        for index in range(len(self.predicted)):
            predicted = self.predicted[index]
            expected = self.expected[index]
            closeness = abs(float(predicted - expected)/expected)
            """
            print 'Predicted: ' + str(predicted)
            print 'Expected: ' + str(expected)
            print 'Closeness: ' + str(closeness)
            stuff = raw_input()
            """
            if closeness < self.threshold:
                numCorrect += 1

        return 100*(float(numCorrect)/len(self.predicted))

    def precision_recall_analysis(self):
        popular = [expected >= settings.POPULAR_SONG_THRESHOLD for expected in self.expected]

        correctly_predicted_popular = 0
        total_popular = 0
        correctly_predicted_unpopular = 0
        total_unpopular = 0
        for index, prediction in enumerate(self.predicted):
            if popular[index]:
                total_popular += 1
            else:
                total_unpopular += 1

            if prediction >= settings.POPULAR_SONG_THRESHOLD and popular[index]:
                correctly_predicted_popular += 1
            elif prediction < settings.POPULAR_SONG_THRESHOLD and not popular[index]:
                correctly_predicted_unpopular += 1

        return float(correctly_predicted_popular)/total_popular, float(correctly_predicted_unpopular)/total_unpopular
