import numpy as np
import pandas as pd
import scipy.spatial
import matplotlib.cm as cm

from components.flowUtils import annotateProgress, cached

class DensityColor:

    def __init__(self, flow):
        self.problems = flow.getProblems()
        self.similarityMatrix = flow.getSimilarityMatrix()

    def problemDensity(self, problem):
        minDistance = float("inf")
        for pid in list(self.similarityMatrix):
            if pid == problem['id']:
                continue
            distance = scipy.spatial.distance.euclidean(self.similarityMatrix[problem['id']], self.similarityMatrix[pid])
            if distance < minDistance:
                minDistance = distance
        return minDistance

    @annotateProgress
    @cached
    def getDensity(self, normalize=True):
        densities = {pid: self.problemDensity(problem) for pid, problem in self.problems.items()}
        if normalize:
            maxDensity = max([density for pid, density in densities.items()])
        else:
            maxDensity = 1.0
        return {pid: density / maxDensity for pid, density in densities.items()}

    @annotateProgress
    @cached
    def getColors(self):
        density = self.getDensity()
        return pd.Series(density.values(), density.keys()).apply(cm.viridis)
