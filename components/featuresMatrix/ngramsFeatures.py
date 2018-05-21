import numpy as np
import itertools
import nltk

from components.flowUtils import annotateProgress, cached

BACKGROUNDS = ['_', 'r', 'g', 'b']
COMMANDS = ['F', 'R', 'L', 'r', 'g', 'b', '1', '2', '3', '4', '5']
BACKGROUNDS_COMMANDS = [a+b for a in BACKGROUNDS for b in COMMANDS]

class NGramsFeatures:

    def __init__(self, flow, n=None):
        if n == None:
            raise AttributeError("Parameter n is missing for NGramsFeatures")

        self.problems = flow.getProblems()
        self.n = n
        self.allNgrams = list(itertools.product(BACKGROUNDS_COMMANDS, repeat=n))

    def getSolutionNgrams(self, solution):
        flattenSolution = [item for sublist in solution for item in sublist]
        ngrams = list(nltk.ngrams(flattenSolution, self.n))
        if len(ngrams) == 0:
            # Hack returning trues when lenght of whole program isnt suffiecient to gnerate any ngrams
            return list(map(lambda ngram: True, self.allNgrams))
        usedNgrams = list(map(lambda ngram: ngram in ngrams, self.allNgrams))
        return usedNgrams

    @annotateProgress
    @cached
    def getFeaturesMatrix(self):
        return {pid: self.getSolutionNgrams(problem['solutions']['most-common']) for pid, problem in self.problems.items()}
