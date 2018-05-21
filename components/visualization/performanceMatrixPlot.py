import numpy as np
import pandas as pd
import pylab as plt
import components.visualization

from components.flowUtils import annotateProgress, cached

class PerformanceMatrixPlot:

    def __init__(self, flow, orderProblems=None, maxUsers=500):
        self.flow = flow
        self.performanceMatrix = flow.getPerformanceMatrix(flow.getProblems())
        self.problems = flow.getProblems()
        self.orderProblems = orderProblems
        self.maxUsers = maxUsers

    @annotateProgress
    @cached
    def getColoredPerformanceMatrix(self):
        pdMatrix = self.performanceMatrix
        if self.orderProblems:
            pdMatrix = pdMatrix.reindex(columns=sorted(pdMatrix.columns, key=lambda pid: self.orderProblems(self.problems[pid]) ))

        if self.maxUsers and pdMatrix.shape[0] > self.maxUsers:
            pdMatrix = pdMatrix.head(self.maxUsers)

        def color(c):
            if np.isnan(c):
                return np.array([1.0, 0.0, 0.0])
            return np.array([c, c, c])

        npMatrix = pdMatrix.applymap(color).as_matrix()

        npMatrix = np.concatenate(npMatrix.flatten())
        npMatrix = np.reshape(npMatrix, (pdMatrix.shape[0], pdMatrix.shape[1], 3))

        return npMatrix

    def plotBase(self):

        plt.imshow(self.getColoredPerformanceMatrix(), interpolation='nearest')
        plt.title(str(self.flow))

    @annotateProgress
    def plot(self):
        self.plotBase()
        plt.show()

    @annotateProgress
    def saveplot(self, path):
        plt.clf()
        self.plotBase()
        plt.savefig(path)
