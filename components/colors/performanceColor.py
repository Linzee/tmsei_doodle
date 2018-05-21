import numpy as np
from colorsys import hls_to_rgb
from copy import copy
import matplotlib.cm as cm

from components.flowUtils import annotateProgress, cached

class PerformanceColor:

    def __init__(self, flow):
        self.problems = flow.getProblems()
        self.similarityMatrix = flow.getSimilarityMatrix()
        self.performanceMatrix = flow.getPerformanceMatrix(flow.getProblems())

    @annotateProgress
    @cached
    def getProblemPerformance(self, normalize=True):
        return self.performanceMatrix.mean()

    @annotateProgress
    @cached
    def getColors(self):
        return self.getProblemPerformance().apply(cm.viridis)
