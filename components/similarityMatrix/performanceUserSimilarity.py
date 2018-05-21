import pandas as pd
import numpy as np

from components.flowUtils import annotateProgress, cached

class PerformanceUserSimilarity:

    def __init__(self, flow, secondLevelOfCorrelation=False):
        self.performanceMatrix = flow.getPerformanceMatrix(flow.getProblems())
        self.problems = flow.getProblems()
        self.secondLevelOfCorrelation = secondLevelOfCorrelation

    @annotateProgress
    @cached
    def getSimilarityMatrix(self):
        simMatrix = self.performanceMatrix.transpose().corr().fillna(0.0)

        if self.secondLevelOfCorrelation:
            simMatrix = simMatrix.corr()

        return simMatrix
