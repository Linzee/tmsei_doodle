import pylab as plt
import components.visualization

from components.flowUtils import annotateProgress, cached

class SimilarityMatrixPlot:

    def __init__(self, flow, orderProblems=None):
        self.similarityMatrix = flow.getSimilarityMatrix()
        self.problems = flow.getProblems()
        self.orderProblems = orderProblems

    def plotBase(self):

        simMatrix = self.similarityMatrix
        if self.orderProblems:
            orderedPorblems = sorted(simMatrix.columns, key=lambda pid: self.orderProblems(self.problems[pid]) )
            simMatrix = simMatrix.reindex(columns=orderedPorblems, index=orderedPorblems)

        plt.imshow(simMatrix, cmap='seismic')

    @annotateProgress
    def plot(self):
        self.plotBase()
        plt.show()

    @annotateProgress
    def saveplot(self, path):
        plt.clf()
        self.plotBase()
        plt.savefig(path)
