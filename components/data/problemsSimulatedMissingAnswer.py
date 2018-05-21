import csv
import pandas as pd
from random import random, shuffle
import numpy as np
from scipy.stats import logistic

from components.flowUtils import annotateProgress, cached

class ProblemsSimulatedMissingAnswer:

    def __init__(self, _, questionCount=100, userCount=1000, questionDifficulty=[0.0], questionSkill=[0.0], probabilitySolvingNextLevel=1.0, lambdaSolvedLevels=None):
        self.questionCount = questionCount
        self.userCount = userCount
        self.questionDifficulty = questionDifficulty
        self.questionSkill = questionSkill
        self.probabilitySolvingNextLevel = probabilitySolvingNextLevel
        self.lambdaSolvedLevels = lambdaSolvedLevels

    @annotateProgress
    @cached
    def getProblems(self):
        problems = {}

        def cycleGen(items, speed):
            i = 0
            while True:
                item = items[i]
                for s in range(speed):
                    yield i, item
                i += 1
                if i >= len(items):
                    i = 0

        getQuestionDifficulty = cycleGen(self.questionDifficulty, 1)
        getQuestionSkill = cycleGen(self.questionSkill, 2)

        for pid in range(1, self.questionCount+1):

            questionDifficultyGroup, questionDifficulty = next(getQuestionDifficulty)
            questionSkillGroup, questionSkill = next(getQuestionSkill)

            problem = {
                'id': pid,
                'title': str(pid),
                'statement': 'none',
                'performance': {},
                'difficulty': np.random.normal(questionDifficulty),
                'difficultyGroup': questionDifficultyGroup,
                'skillGroup': questionSkillGroup
            }
            problems[pid] = problem

        userSkills = np.random.normal(size=(self.userCount, len(self.questionSkill)))

        for u in range(self.userCount):

            if self.lambdaSolvedLevels:
                groups = self.lambdaSolvedLevels(u)
            else:
                groups = []
                allGroups = list(range(len(self.questionDifficulty)))
                shuffle(allGroups)
                for group in allGroups:
                    groups.append(group)
                    if random() > self.probabilitySolvingNextLevel:
                        break

            for problem in problems.values():

                if problem['difficultyGroup'] not in groups:
                    continue

                a = np.random.random()
                r = logistic.cdf(userSkills[u, problem['skillGroup']] - problem['difficulty'])
                problem['performance'][u] = 1.0 if a >= r else 0.0

        return problems

    @annotateProgress
    @cached
    def getPerformanceMatrix(self, problems):
        return pd.DataFrame( {pid: problem['performance'] for pid, problem in problems.items()}, columns=[pid for pid, problem in problems.items()] ).to_sparse()
