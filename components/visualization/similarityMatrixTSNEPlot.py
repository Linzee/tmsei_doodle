from components.visualization.similarityMatrixProjectionPlot import SimilarityMatrixProjectionPlot
from sklearn.manifold import TSNE

from components.flowUtils import annotateProgress, cached

class SimilarityMatrixTSNEPlot(SimilarityMatrixProjectionPlot):

    def __init__(self, flow, annotate=1.0, learning_rate=200, n_iter=16000):
        super().__init__(flow, annotate)
        self.learning_rate = learning_rate
        self.n_iter = n_iter

    @annotateProgress
    @cached
    def getProjection(self):
        model = TSNE(learning_rate = self.learning_rate, n_iter=self.n_iter)
        return model.fit_transform(self.similarityMatrix)
