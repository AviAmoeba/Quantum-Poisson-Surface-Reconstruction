import numpy as np
import math

def gaussian(r2, sigma):
    value = np.exp( -r2 / (2 * sigma**2) )
    return value

def truncated_gaussian(r2, sigma):
    print()

def wendland_0(r2):
    r = math.sqrt(r2)
    value = ( 1 - r )
    return value
