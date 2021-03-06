import numpy as np
import pandas as pd
from unidecode import unidecode
from pylab import plt

# Components initialization
from components.flow import Flow

from components.customizable.customComponent import CustomComponent

from components.data.problemsJson import ProblemsJson
from components.data.filterProblems import FilterProblems
from components.data.problemsSimulatedMissingAnswer import ProblemsSimulatedMissingAnswer
from components.data.problemsSimulatedDefaultAnswer import ProblemsSimulatedDefaultAnswer

from components.featuresMatrix.problemSolutionFeatures import ProblemSolutionFeatures
from components.featuresMatrix.ngramsFeatures import NGramsFeatures
from components.featuresMatrix.normalizeLog import NormalizeLog
from components.featuresMatrix.problemStatementFeatures import ProblemStatementFeatures
from components.featuresMatrix.userPerformanceFeatures import UserPerformanceFeatures

from components.similarityMatrix.featuresSimilarity import FeaturesSimilarity
from components.similarityMatrix.stringEditDistanceSimilarity import StringEditDistanceSimilarity
from components.similarityMatrix.performanceSimilarity import PerformanceSimilarity
from components.similarityMatrix.booleanPerformanceSimilarity import BooleanPerformanceSimilarity
from components.similarityMatrix.combinedSimilarity import CombinedSimilarity
from components.similarityMatrix.performanceUserSimilarity import PerformanceUserSimilarity

from components.strings.statementString import StatementString
from components.strings.mostCommonSolutionString import MostCommonSolutionString

from components.visualization.similarityMatrixPlot import SimilarityMatrixPlot
from components.visualization.similarityMatrixTSNEPlot import SimilarityMatrixTSNEPlot
from components.visualization.similarityMatrixPCAPlot import SimilarityMatrixPCAPlot
from components.visualization.performanceMatrixPlot import PerformanceMatrixPlot
from components.visualization.performanceUserMatrixPlot import PerformanceUserMatrixPlot
from components.visualization.itemHistogramPlot import ItemHistogramPlot

from components.colors.densityColor import DensityColor
from components.colors.lambdaColor import LambdaColor
from components.colors.lambdaProblemColor import LambdaProblemColor
from components.colors.performanceColor import PerformanceColor
from components.colors.totalSimilarityColor import TotalSimilarityColor

from components.markers.lambdaMarker import LambdaMarker
from components.markers.lambdaProblemMarker import LambdaProblemMarker

from components.umimeCesky.problemsUmime import ProblemsUmime
from components.umimeCesky.performanceMatrixNormalization import PerformanceMatrixNormalization
from components.umimeCesky.constants import *
from components.umimeCesky.utils import *
