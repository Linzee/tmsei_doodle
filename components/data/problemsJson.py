import json
from glob import glob
import re
import pandas as pd
import os

from components.flowUtils import annotateProgress, cached

DATA_DIR = os.path.dirname(os.path.abspath(__file__))+'/../../data/'

class ProblemsJson:

    def __init__(self, flow, dataPath = DATA_DIR+'robotanik'):
        self.dataPath = dataPath

    def getProblemId(self, filePath):
        m = re.match(self.dataPath+"/(.*?).json", filePath)
        if m:
            return int(m.group(1))
        else:
            raise ValueError('Cannot parse problem id')

    @annotateProgress
    @cached
    def getProblems(self):
        problems = {}

        for filePath in glob(self.dataPath+"/*.json"):
            with open(filePath, 'r') as infile:
                pid = self.getProblemId(filePath)
                problems[pid] = json.load(infile)
                problems[pid]['id'] = pid

        if len(problems) == 0:
            raise ValueError('No problems found in "'+self.dataPath+'"')

        return problems

    @annotateProgress
    @cached
    def getPerformanceMatrix(self, problems):
        itemsWithPerformance = filter(lambda item: len(item[1]['performance']) > 0, problems.items())
        df = pd.DataFrame( {pid: problem['performance'] for pid, problem in itemsWithPerformance} ).to_sparse()

        return df
