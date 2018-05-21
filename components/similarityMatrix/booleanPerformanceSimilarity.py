import pandas as pd
import numpy as np
from math import sqrt

from components.flowUtils import annotateProgress, cached

class BooleanPerformanceSimilarity:

    def __init__(self, flow, similarityMetric='pearson', secondLevelOfCorrelation=False):
        self.performanceMatrix = flow.getPerformanceMatrix(flow.getProblems())
        self.problems = flow.getProblems
        self.similarityMetric = similarityMetric
        self.secondLevelOfCorrelation = secondLevelOfCorrelation

    @annotateProgress
    @cached
    def getSimilarityMatrix(self):

        similarityMetrics = {
            'pearson': lambda a,b,c,d: (a*d-b*c)/sqrt((a+b)*(a+c)*(b+d)*(c+d)),
            'yule': lambda a,b,c,d: (a*d-b*c)/(a*d+b*c),
            'jaccard': lambda a,b,c,d: a/(a+b+c),
            'sokal': lambda a,b,c,d: (a+d)/(a+b+c+d),
            'cosine': lambda a,b,c,d: a/sqrt((a+b)*(a+c)),
        }

        simMatrix = pd.DataFrame(np.zeros((len(list(self.performanceMatrix)), len(list(self.performanceMatrix)))), columns=list(self.performanceMatrix), index=list(self.performanceMatrix), dtype=np.float64)

        for pid1 in list(self.performanceMatrix):
            for pid2 in list(self.performanceMatrix):
                p1 = self.performanceMatrix[pid1]
                p2 = self.performanceMatrix[pid2]

                ic = p1 + 2 * p2
                icv = ic.value_counts()

                a = icv[0.0] if 0.0 in icv else 0
                b = icv[1.0] if 1.0 in icv else 0
                c = icv[2.0] if 2.0 in icv else 0
                d = icv[3.0] if 3.0 in icv else 0

                simMatrix.loc[pid1, pid2] = similarityMetrics[self.similarityMetric](a, b, c, d)

        if self.secondLevelOfCorrelation:
            simMatrix = simMatrix.corr()

        return simMatrix
