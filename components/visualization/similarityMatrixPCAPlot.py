from sklearn.decomposition import PCA
from components.visualization.similarityMatrixProjectionPlot import SimilarityMatrixProjectionPlot
import numpy as np

from components.flowUtils import annotateProgress, cached

class SimilarityMatrixPCAPlot(SimilarityMatrixProjectionPlot):

    def __init__(self, flow, annotate=1.0, display_dimensions=(0, 1)):
        super().__init__(flow, annotate)
        self.display_dimensions = display_dimensions

    @annotateProgress
    @cached
    def getProjection(self):

        model = PCA(n_components= (1+max(self.display_dimensions[0], self.display_dimensions[1])) )

        results = model.fit(self.similarityMatrix)

        return np.transpose([results.components_[self.display_dimensions[0]], results.components_[self.display_dimensions[1]]])
