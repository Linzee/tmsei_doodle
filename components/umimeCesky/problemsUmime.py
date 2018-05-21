import os
import csv
import pandas as pd
import numpy as np

from components.flowUtils import annotateProgress, cached

DATA_DIR = os.path.dirname(os.path.abspath(__file__))+'/../../data/'

FILE_ITEMS = 'nova_doplnovacka_questions.csv'
FILE_LOG = 'nova_doplnovacka_log.csv'
FILE_TAXONOMY = 'system_kc.csv'
FILE_ITEMS_PS = 'system_ps_problem.csv'
FILE_PS = 'system_ps.csv'

class ProblemsUmime:

    def __init__(self, _, dataPath = DATA_DIR+'cestina', maxProblems=False, maxLogs=False, includeHidden=False, includeUnlinked=False, useLastAnswer=False):
        self.dataPath = dataPath
        self.maxProblems = maxProblems
        self.maxLogs = maxLogs
        self.includeHidden = includeHidden
        self.includeUnlinked = includeUnlinked
        self.useLastAnswer = useLastAnswer

    def parseText(self, text):
        if text.startswith('[["text"'):
            return text[10:-3]
        return text

    @annotateProgress
    @cached
    def getProblems(self):

        problems = {}

        with open(self.dataPath + "/" + FILE_ITEMS, 'r') as problemsFile:
            problemsReader = csv.reader(problemsFile, delimiter=';', quotechar='|')
            next(problemsReader) #read header
            for row in problemsReader:

                if not self.includeHidden and int(row[7]) == 0:
                    continue

                problem = {
                    'id': int(row[0]),
                    'title': self.parseText(row[1]),
                    'statement': self.parseText(row[1]),
                    'solution': self.parseText(row[2]),
                    'distractor': self.parseText(row[3]),
                    'performance': {},
                    'pss': []
                }
                problems[int(row[0])] = problem

                if self.maxProblems and len(problems) >= self.maxProblems:
                    break

        if not problems:
            raise ValueError('No problems found in "'+self.dataPath+'"')

        with open(self.dataPath + "/" + FILE_LOG, 'r') as logFile:
            logReader = csv.reader(logFile, delimiter=';', quotechar='|')
            next(logReader) #read header

            i=0
            for row in logReader:
                if int(row[2]) not in problems:
                    continue

                problem = problems[int(row[2])]
                if self.useLastAnswer or not int(row[1]) in problem['performance']:
                    problem['performance'][int(row[1])] = float(row[3]) # float(row[3])

                i += 1
                if self.maxLogs and i > self.maxLogs:
                    break

        psData = {}

        with open(self.dataPath + "/" + FILE_PS, 'r') as psFile:
            psReader = csv.reader(psFile, delimiter=';', quotechar='|')
            next(psReader) #read header
            for row in psReader:
                psData[int(row[0])] = {
                    'taxonomy': int(row[1]),
                    'class': int(row[6]),
                    'grade': int(row[5])
                }

        with open(self.dataPath + "/" + FILE_ITEMS_PS, 'r') as itemsPsFile:
            itemsPsReader = csv.reader(itemsPsFile, delimiter=';', quotechar='|')
            next(itemsPsReader) #read header
            for row in itemsPsReader:
                if int(row[2]) in problems and int(row[1]) in psData:
                    problems[int(row[2])]['pss'].append(int(row[1]))
                    for key in ['taxonomy', 'class', 'grade']:
                        problems[int(row[2])][key] = psData[int(row[1])][key]

        if not self.includeUnlinked:
            problems = {pid: problem for pid, problem in problems.items() if problem['pss']}

        return problems

    @annotateProgress
    @cached
    def getPerformanceMatrix(self, problems):
        return pd.DataFrame( {pid: problem['performance'] for pid, problem in problems.items()}, columns=[pid for pid, problem in problems.items()] ).to_sparse()

    @annotateProgress
    @cached
    def getTaxonomy(self):
        items = {}

        with open(self.dataPath + "/" + FILE_TAXONOMY, 'r') as taxonomyFile:
            taxonomyReader = csv.reader(taxonomyFile, delimiter=';', quotechar='|')
            next(taxonomyReader) #read header
            for row in taxonomyReader:
                items[int(row[0])] = {
                    'id': int(row[0]),
                    'title': row[2],
                    'parent': int(row[1]),
                    'children': None
                }

        def constructTree(parent):
            children = []
            for id, item in items.items():
                if item['parent'] == parent:
                    item['children'] = constructTree(item['id'])
                    children.append(item)
            return children

        return constructTree(0)
