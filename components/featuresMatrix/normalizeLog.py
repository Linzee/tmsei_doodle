import numpy as np

from components.flowUtils import annotateProgress, cached

class NormalizeLog:

    def __init__(self, flow):
        self.features = flow.getFeaturesMatrix()

    @annotateProgress
    @cached
    def getFeaturesMatrix(self):
        return {pid: np.log(features + 1) for pid, features in self.features.items()}
