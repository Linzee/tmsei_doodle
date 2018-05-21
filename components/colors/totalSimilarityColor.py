import numpy as np
from colorsys import hls_to_rgb
from copy import copy
import matplotlib.cm as cm

from components.flowUtils import annotateProgress, cached

class TotalSimilarityColor:

    def __init__(self, flow):
        self.problems = flow.getProblems()
        self.similarityMatrix = flow.getSimilarityMatrix()

    @annotateProgress
    @cached
    def getTotalSimilarity(self, normalize=True):
        totalSimilarities = self.similarityMatrix.apply(lambda col: col.sum(), reduce=True)
        return totalSimilarities / totalSimilarities.max() if normalize else totalSimilarities

    @annotateProgress
    @cached
    def getColors(self):
        return self.getTotalSimilarity().apply(cm.viridis)
