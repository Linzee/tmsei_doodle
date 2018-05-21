import numpy as np

from components.flowUtils import annotateProgress, cached

class ProblemStatementFeatures:

    def __init__(self, flow):
        self.problems = flow.getProblems()

    def geStatementFeaturesMap(self, features, statement):
        statementIndexes = list(map(lambda c: features.index(c), statement))
        return np.histogram(statementIndexes, len(features), density=True)[0]

    def detectFeaturesList(self, statements):
        features = set()
        for statement in statements:
            features = features.union(set(statement))
        return list(features)

    @annotateProgress
    @cached
    def getFeaturesMatrix(self):
        features = self.detectFeaturesList([problem['statement'] for pid, problem in self.problems.items()])
        return {pid: self.geStatementFeaturesMap(features, problem['statement']) for pid, problem in self.problems.items()}
