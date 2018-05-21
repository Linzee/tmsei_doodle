import pandas as pd

from components.flowUtils import annotateProgress, cached

class LambdaProblemMarker:

    def __init__(self, flow, lambdaMarker=None):
        self.lambdaMarker = lambdaMarker
        self.similarityMatrix = flow.getSimilarityMatrix()
        self.problems = flow.getProblems()

    @annotateProgress
    @cached
    def getMarkers(self):
        return pd.Series(list(self.similarityMatrix), list(self.similarityMatrix)).apply(lambda pid: self.lambdaMarker(self.problems[pid]))
