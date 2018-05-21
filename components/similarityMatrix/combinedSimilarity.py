import pandas as pd

from components.flowUtils import annotateProgress, cached

class CombinedSimilarity:

    def __init__(self, *metrics, combineMethod='mean'):
        self.metrics = metrics
        self.combineMethod = combineMethod

    @annotateProgress
    @cached
    def getSimilarityMatrix(self):
        dfs = [metric.getSimilarityMatrix().to_dense() for metric in self.metrics]
        df_concat = pd.concat(dfs)
        by_row_index = df_concat.groupby(df_concat.index)
        for method in [self.combineMethod]:
            if method == 'mean':
                df_means = by_row_index.mean()
                break
            if method == 'min':
                exit()
                df_means = by_row_index.min()
                break
            if method == 'max':
                df_means = by_row_index.max()
                break
            raise AttributeError("Combine method not defined")
        return df_means.head()
