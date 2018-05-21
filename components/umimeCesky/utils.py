
def filterProblemsByConcept(pss):
    pss_global = pss
    return lambda problem: [x for x in pss_global if x in problem['pss']]
