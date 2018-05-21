import pandas as pd
import editdistance

from components.flowUtils import annotateProgress, cached

class StringEditDistanceSimilarity:

    def __init__(self, flow):
        self.strings = flow.getStrings()

    def stringSimilarity(self, s1, s2):
        return 1 / (1 + editdistance.eval(s1, s2))

    @annotateProgress
    @cached
    def getSimilarityMatrix(self):

        problems_count = len(self.strings)

        similarityMatrix = pd.DataFrame(columns=list(self.strings))

        for pid, s1 in self.strings.items():
            print(pid)
            similarityMatrix[pid] = [self.stringSimilarity(s1, s2) for pid, s2 in self.strings.items()]

        return similarityMatrix
