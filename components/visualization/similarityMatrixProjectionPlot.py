import pylab as plt
from random import random
import components.visualization

from components.flowUtils import annotateProgress, cached

class SimilarityMatrixProjectionPlot:

    def __init__(self, flow, annotate=1.0):
        self.flow = flow
        self.problems = flow.getProblems()
        self.colors = flow.getColors() if hasattr(flow, 'getColors') else None
        self.markers = flow.getMarkers() if hasattr(flow, 'getMarkers') else None
        self.similarityMatrix = flow.getSimilarityMatrix()
        self.annotate = annotate

    def getProjection(self):
        raise NotImplementedError("You have to use concrete projection class, this is abstract base class")

    def plotBase(self):

        projection = self.getProjection()

        i = 0
        for cid in list(self.similarityMatrix):

            x, y = projection[i]

            marker = "o"
            if self.markers is not None:
                marker = self.markers[cid]

            color = None
            if self.colors is not None:
                color = self.colors[cid]

            plt.plot(x, y, marker, color=color)

            if random() < self.annotate:
                plt.text(x, y, self.problems[cid]['title'], alpha=0.5)

            i += 1

        # indexBic = 0
        # indexBicik = 0
        # for index, problem in enumerate(self.problems.values()):
        #     if problem['statement'] == 'b_č':
        #         indexBic = index
        #     if problem['statement'] == 'b_čík':
        #         indexBicik = index
        # plt.plot([projection[indexBic][0], projection[indexBicik][0]], [projection[indexBic][1], projection[indexBicik][1]], c='black')

        plt.title(str(self.flow))

    def plot(self):
        self.plotBase()
        plt.show()

    def saveplot(self, path):
        plt.clf()
        self.plotBase()
        plt.savefig(path)
