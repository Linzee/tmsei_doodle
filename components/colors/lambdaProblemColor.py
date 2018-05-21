import pandas as pd

from components.flowUtils import annotateProgress, cached

class LambdaProblemColor:

    def __init__(self, flow, lambdaColor=None):
        self.lambdaColor = lambdaColor
        self.similarityMatrix = flow.getSimilarityMatrix()
        self.problems = flow.getProblems()

    @annotateProgress
    @cached
    def getColors(self):
        return pd.Series(list(self.similarityMatrix), list(self.similarityMatrix)).apply(lambda pid: self.lambdaColor(self.problems[pid]))
