import scipy.spatial
import scipy.stats
import numpy as np

def euclideanSimilarity(f1, f2):
    return 1 / (1 + scipy.spatial.distance.euclidean(f1, f2))

def cosineSimilarity(f1, f2):
    return 1 - scipy.spatial.distance.cosine(f1, f2)

def jaccardSimilarity(f1, f2):
    return 1 - scipy.spatial.distance.jaccard(f1, f2)

def correlationSimilarity(f1, f2):
    t1 = []
    t2 = []

    if isinstance(f1, dict):
        #sparse
        for key, v in f1.items():
            if key in f2:
                t1.append(v)
                t2.append(f2[key])

    else:
        for i in range(len(f1)):
            if not np.isnan(f1[i]) and not np.isnan(f2[i]):
                t1.append(f1[i])
                t2.append(f2[i])

    if len(t1) == 0:
        return 0.0

    return scipy.spatial.distance.correlation(np.array(t1).astype(np.float), np.array(t2).astype(np.float))

def spearmanSimilarity(f1, f2):
    t1 = []
    t2 = []

    for i in range(len(f1)):
        if not np.isnan(f1[i]) and not np.isnan(f2[i]):
            t1.append(f1[i])
            t2.append(f2[i])

    if len(t1) == 0:
        return 0.0

    return scipy.stats.spearmanr(t1, t2)[0]
