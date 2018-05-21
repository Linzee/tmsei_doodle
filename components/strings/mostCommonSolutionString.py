import numpy as np
import functools

class MostCommonSolutionString:

    def __init__(self, flow):
        self.problems = flow.getProblems()

    def getSolutionString(self, solution):
        flattenSolution = [item for sublist in solution for item in sublist]
        flattenSolution = [item for sublist in flattenSolution for item in sublist]
        return ''.join(flattenSolution)

    @functools.lru_cache()
    def getStrings(self):
        return {pid: self.getSolutionString(problem['solutions']['most-common']) for pid, problem in self.problems.items()}
