import numpy as np
import pandas as pd
import pylab as plt
import components.visualization

from components.flowUtils import annotateProgress, cached

class PerformanceUserMatrixPlot:

    def __init__(self, flow, orderUsers=None):
        self.flow = flow
        self.performanceMatrix = flow.getPerformanceMatrix(flow.getProblems())
        self.orderUsers = orderUsers

    def plotBase(self):

        pdMatrix = self.performanceMatrix.transpose()
        if self.orderUsers:
            pdMatrix = pdMatrix.reindex(columns=sorted(pdMatrix.columns, key=lambda uid: self.orderUsers(uid) ))

        def color(c):
            if np.isnan(c):
                return np.array([1.0, 0.0, 0.0])
            return np.array([c, c, c])

        # pdMatrix = pdMatrix.head(100)

        npMatrix = pdMatrix.applymap(color).as_matrix()

        npMatrix = np.concatenate(npMatrix.flatten())
        npMatrix = np.reshape(npMatrix, (pdMatrix.shape[0], pdMatrix.shape[1], 3))

        plt.imshow(npMatrix, interpolation='nearest')
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
