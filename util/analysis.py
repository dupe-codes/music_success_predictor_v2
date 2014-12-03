"""
Defines an analysis class to analyze algorithm results
"""

class AnalysisUtil(object):

    def __init__(self, expected, predicted, threshold=0.1):
        """
        Initializes object to analyze given data

        Params: expected - dict of song title => actual scores
                predicted - dict of song title => predicted scores
        """
        self.expected = expected
        self.predicted = predicted
        self.threshold = threshold

    def percentage_accuracy(self):
        """ Returns the ratio of accurately predicted scores """
        numCorrect = 0
        for song, predicted in self.predicted.iteritems():
            expected_val = self.expected[song]
            if abs(predicted - expected_val) < self.threshold:
                numCorrect += 1
        return 100*(float(numCorrect)/len(self.predicted))
