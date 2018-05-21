from components.flowUtils import annotateProgress, cached

import types

class FilterProblems:

    def __init__(self, flow, filterProblems = None, filterUsers = None):
        self.filterProblems = filterProblems
        self.filterUsers = filterUsers
        self.problems = flow.getProblems()
        self.performanceMatrix = flow.getPerformanceMatrix(self.getProblems())

    @annotateProgress
    @cached
    def getProblems(self):
        return {pid: problem for pid, problem in self.problems.items() if self.filterProblems == None or self.filterProblems(problem)}

    @annotateProgress
    @cached
    def getPerformanceMatrix(self, problems):
        if self.filterUsers:

            usersSelector = self.filterUsers
            if type(self.filterUsers) is types.LambdaType:
                usersSelector = [self.filterUsers(user) for user in self.performanceMatrix.index]

            return self.performanceMatrix[usersSelector]
        else:
            return self.performanceMatrix
