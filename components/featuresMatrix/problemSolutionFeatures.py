import numpy as np

from components.flowUtils import annotateProgress, cached

BACKGROUNDS = ['_', 'r', 'g', 'b']
COMMANDS = ['F', 'R', 'L', 'r', 'g', 'b', '1', '2', '3', '4', '5']
BACKGROUNDS_COMMANDS = [a+b for a in BACKGROUNDS for b in COMMANDS]
BACKGROUNDS_PLUS_COMMANDS = BACKGROUNDS + COMMANDS

class ProblemSolutionFeatures:

    def __init__(self, flow, solutionConditionPairs = True, solutionBoolean=False):
        self.problems = flow.getProblems()
        self.solutionConditionPairs = solutionConditionPairs
        self.solutionBoolean = solutionBoolean

    def getSolutionFeatures(self, solution):
        flattenSolution = [item for sublist in solution for item in sublist]
        if not self.solutionConditionPairs:
            flattenSolution = [item for sublist in flattenSolution for item in sublist]

        commandsList = BACKGROUNDS_COMMANDS if self.solutionConditionPairs else BACKGROUNDS_PLUS_COMMANDS

        if self.solutionBoolean:
            return np.fromiter(map(lambda c : 1 if c in flattenSolution else 0, commandsList), dtype=np.int)
        else:
            solutionIndexes = list(map(lambda c: commandsList.index(c), flattenSolution))
            return np.histogram(solutionIndexes, len(commandsList), density=True)[0]

    @annotateProgress
    @cached
    def getFeaturesMatrix(self):
        return {pid: self.getSolutionFeatures(problem['solutions']['most-common']) for pid, problem in self.problems.items()}
