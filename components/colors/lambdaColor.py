import numpy as np
import pandas as pd

from components.flowUtils import annotateProgress, cached

class LambdaColor:

    def __init__(self, flow, lambdaColor=None):
        self.lambdaColor = lambdaColor
        self.similarityMatrix = flow.getSimilarityMatrix()

    @annotateProgress
    @cached
    def getColors(self):
        return pd.Series(list(self.similarityMatrix), list(self.similarityMatrix)).apply(self.lambdaColor)
