import numpy as np

# units are in milimeters
# TRAJ_STEP_MIN = 0.1
# TRAJ_STEP_MAX = 20.
# TRAJ_STEP_INC = 0.1
TRAJ_STEP_MIN = 0.1
TRAJ_STEP_MAX = 100.
TRAJ_STEP_INC = 0.1

MIN_STEP = 0.1
MAX_STEP = 100.

DT_VAL = 20
MIN_DT = np.radians(-DT_VAL)
MAX_DT = np.radians(DT_VAL)



def scale(min_ini, max_ini, min_fin, max_fin, x):
    # rescale x from a initial range to a final range
    p = float(max_fin - min_fin)/float(max_ini - min_ini)
    d = min_fin - (min_ini * p)
    return np.float64((x*p) + d)

def normal_in_range(ini, fin):
    r = -10
    while r < -1 or r > 1: # or r == 0.0:
        r = np.random.normal(0, 0.33, 1)[0]

    # if r > 0.:
    #     r = 1 - r
    # else:
    #     r = -1 - r
    return scale(-1.0, 1.0, ini, fin, r)