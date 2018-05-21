from components.flowUtils import annotateProgress, cached

class UserPerformanceFeatures:

    def __init__(self, flow):
        self.problems = flow.getProblems()

    @annotateProgress
    @cached
    def getFeaturesMatrix(self):
        return {pid: problem['performance'] for pid, problem in self.problems.items()}
