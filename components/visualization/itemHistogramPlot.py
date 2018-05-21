import numpy as np
import pandas as pd
import pylab as plt
import components.visualization

from components.flowUtils import annotateProgress, cached

class ItemHistogramPlot:

    def __init__(self, flow, histogramProperty=None, histogramGroupBy=None, histogramColors=None):
        self.flow = flow
        self.problems = flow.getProblems()
        self.histogramProperty = histogramProperty
        self.histogramGroupBy = histogramGroupBy
        self.histogramColors = histogramColors

    @annotateProgress
    @cached
    def getHistogramData(self):
        df = pd.DataFrame([list(self.problems.keys())], ['problems'], list(self.problems.keys())).transpose()
        df = df.apply(self.histogramProperty)
        df = df.groupby(self.histogramGroupBy, axis=0)
        df = list(df)
        df = pd.DataFrame([a[1].apply(lambda b: b[0], axis=1) for a in df], [a[0] for a in df]).transpose()
        return df

    def plotBase(self):

        data = self.getHistogramData()

        for answer in list(data):
            c = None if self.histogramColors is None else self.histogramColors[answer]
            plt.hist(data[answer], 20, (0.0, 1.0), alpha=0.5, histtype = 'step', label=answer, linewidth=2.0, color=c)
        plt.title(str(self.flow))
        plt.legend()

    @annotateProgress
    def plot(self):
        self.plotBase()
        plt.show()

    @annotateProgress
    def saveplot(self, path):
        plt.clf()
        self.plotBase()
        plt.savefig(path)
