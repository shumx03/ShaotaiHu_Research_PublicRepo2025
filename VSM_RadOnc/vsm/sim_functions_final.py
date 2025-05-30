"""
Similiarty Functions
Created on Monday Feb 10 20:00:39 2025
@authors: Samuel luk, Shaotai Hu
"""

### Packages ###
import numpy as np
import pandas as pd
import math
from numpy import dot
from numpy.linalg import norm
#from scipy.spatial import distance
#import Levenshtein

### cosine similarity ###
def cos_sim(vec1, vec2):
    val = np.dot(vec1, vec2)/(norm(vec1)*norm(vec2))
    return val

### Euclidean Distance ###
def eud_dis(vec1, vec2):
    # scaling by norm
    # max euclidean distance between two normalized vectors is 2
    norm1 = np.array(vec1)/np.linalg.norm(vec1)
    norm2 = np.array(vec2)/np.linalg.norm(vec2)
    dis = (np.linalg.norm(norm1 - norm2))
    return dis

### Manhatten Distance ###
def man_dis(vec1, vec2):
    # scaling by norm
    # max manhattan distance between two normalized vector is 2*len(vec)
    norm1 = np.array(vec1)/np.linalg.norm(vec1)
    norm2 = np.array(vec2)/np.linalg.norm(vec2)
    dis = (np.sum(np.abs(norm1 - norm2)))
    return dis

"""
# Minkowski Distance:
# p = 1 manhattan distance, p = 2 euclidean distance, p > 2 generalized minkowski distance
# p is the order of Minkowshi distance
# max minkowski distance between two normalized vector is (len(vec)*(2**p))**(1/3)
def mik_dis(vec1, vec2, p):
    arr1 = np.array(vec1)/np.linalg.norm(vec1)
    arr2 = np.array(vec2)/np.linalg.norm(vec2)
    #scale = (len(vec1)*(2**p))**(1/3)
    dis = (np.sum(np.abs(arr1-arr2) ** p) ** (1/p))
    return dis
""";
