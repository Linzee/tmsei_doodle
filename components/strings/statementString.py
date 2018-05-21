import numpy as np

from components.flowUtils import annotateProgress, cached

class StatementString:

    def __init__(self, flow):
        self.problems = flow.getProblems()

    @annotateProgress
    @cached
    def getStrings(self):
        return {pid: problem['statement'] for pid, problem in self.problems.items()}
