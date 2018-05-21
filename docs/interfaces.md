# Interfaces

## Data

**getProblems** returns dictionary of pid (problem id) => problem. Each problem is dictionary of its attributes (pid, statement, solution, performance, ..).

**getPerformanceMatrix** returns pandas DataFrame containing performance matrix (items x users). Method has one argument '''problems''' for filtering which problems to include in performance matrix.

## FeaturesMatrix

**getFeaturesMatrix** returns pandas DataFrame containing features matrix (items x features).

## SimilarityMatrix

**getSimilarityMatrix** returns pandas DataFrame containing similarity matrix (item x item).

## Colors

**getColors** returns pandas Series indexed by item pid. Values are valid matplotlib colors.

## Markers

**getMarkers** returns pandas Series indexed by item pid. Values are valid matplotlib markers.

## Visualisation

**plot** displays some visualization of data.

**saveplot** saves visualization to file.

**getProjection** is method present in projections and returns list of item (x,y) coordinates.
