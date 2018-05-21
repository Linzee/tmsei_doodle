import pandas as pd

from components.flowUtils import annotateProgress, cached

class FeaturesSimilarity:

    def __init__(self, flow, similarityMetric=None):
        if similarityMetric == None:
            raise AttributeError("Parameter similarityMetric is missing for FeaturesSimilarity")

        self.featuresMatrix = flow.getFeaturesMatrix()
        self.similarityMetric = similarityMetric

    @annotateProgress
    @cached
    def getSimilarityMatrix(self):

        problems_count = len(self.featuresMatrix)

        similarityMatrix = pd.DataFrame(columns=list(self.featuresMatrix))

        for pid, f1 in self.featuresMatrix.items():
            similarityMatrix[pid] = [self.similarityMetric(f1, f2) for pid, f2 in self.featuresMatrix.items()]

        return similarityMatrix
