import pandas as pd

from components.flowUtils import annotateProgress, cached

class LambdaMarker:

    def __init__(self, flow, lambdaMarker=None):
        self.lambdaMarker = lambdaMarker
        self.similarityMatrix = flow.getSimilarityMatrix()

    @annotateProgress
    @cached
    def getMarkers(self):
        return pd.Series(list(self.similarityMatrix), list(self.similarityMatrix)).apply(self.lambdaMarker)
