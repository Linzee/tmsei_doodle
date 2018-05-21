import pandas as pd
import numpy as np
from unidecode import unidecode

from components.flowUtils import annotateProgress, cached

class PerformanceMatrixNormalization:

    def __init__(self, flow, normalizeAnswers = False, normalizeAnswersTreshold=None, normalizeAnswersToAscii=True, normalizeLevels = False, levelsPss=[]):
        self.flow = flow
        self.normalizeAnswers = normalizeAnswers
        self.normalizeAnswersTreshold = normalizeAnswersTreshold
        self.normalizeAnswersToAscii = normalizeAnswersToAscii
        self.normalizeLevels = normalizeLevels
        self.levelsPss = levelsPss
        self.myFlowIndex = len(flow.cascades)

        if self.normalizeLevels and not self.levelsPss:
            raise ValueError('levelsPss has to be given to normalize levels')

    @annotateProgress
    @cached
    def getPerformanceMatrix(self, problems):
        problems = self.flow.lookup('getProblems', self.myFlowIndex)()
        perfMatrix = self.flow.lookup('getPerformanceMatrix', self.myFlowIndex)(problems)

        if self.normalizeAnswers:
            perfMatrix = perfMatrix.to_dense()
            problemSolution = lambda pid: unidecode(problems[pid]['solution']) if self.normalizeAnswersToAscii else problems[pid]['solution']
            userAnswerPerformanceMatrix = perfMatrix.groupby(problemSolution, axis=1).mean()
            userAnswerDifference = userAnswerPerformanceMatrix.apply(lambda row: row.max() - row.min(), axis=1)

            if self.normalizeAnswersTreshold:
                filterValue = self.normalizeAnswersTreshold
            else:
                filterValue = userAnswerDifference.median()

            perfMatrix = perfMatrix[userAnswerDifference < filterValue]

        if self.normalizeLevels:
            problemsPs = pd.Series([ [x for x in self.levelsPss if x in problems[pid]['pss']][0] for pid in list(perfMatrix) ], list(perfMatrix))
            userGroups = perfMatrix.apply(lambda row: sum([(2 ** i) * (1 if sum(problemsPs[row.notnull()] == self.levelsPss[i]) > 30 else 0) for i in range(len(self.levelsPss)) ]), axis=1, reduce=True)

            perfMatrix = perfMatrix.apply(lambda col: col.where(np.bitwise_and(userGroups, [1,2,4][self.levelsPss.index(problemsPs[col.name])]) != 0))

        return perfMatrix
