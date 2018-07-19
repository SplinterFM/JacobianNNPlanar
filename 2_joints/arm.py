from point2 import Point2
import numpy as np
from helper import scale

MAX_THETA = np.pi
MIN_THETA = -np.pi

class Arm:
    def __init__(self, l1=300, l2=300, t1=0.0, t2=np.pi/2.):
        self.t1 = t1
        self.t2 = t2
        self.l1 = l1
        self.l2 = l2

    def move(self, dt1, dt2):
        self.t1 += dt1
        self.t2 += dt2

        if self.t1 > MAX_THETA:
            self.t1 -= 2*np.pi
        if self.t2 > MAX_THETA:
            self.t2 -= 2*np.pi

        if self.t1 < MIN_THETA:
            self.t1 += 2*np.pi
        if self.t2 < MIN_THETA:
            self.t2 += 2*np.pi

    def endeffector(self):
        p1 = Point2().polar(self.l1, self.t1)
        return Point2().polar(self.l2, self.t2+self.t1) + p1

    def set_random_pose(self):
        t1 = scale(0.0, 1.0, MIN_THETA, MAX_THETA, np.random.random())
        t2 = scale(0.0, 1.0, MIN_THETA, MAX_THETA, np.random.random())
        # check if the values are between MIN_THETA and MAX_THETA
        assert t1 > MIN_THETA and t1 < MAX_THETA
        assert t2 > MIN_THETA and t2 < MAX_THETA
        # if they are, set joints to the values
        self.t1 = t1
        self.t2 = t2

    def get_normalized_pose(self):
        t1 = scale(MIN_THETA, MAX_THETA, 0.0, 1.0, self.t1)
        t2 = scale(MIN_THETA, MAX_THETA, 0.0, 1.0, self.t2)
        # check if the values are between 0.0 and 1.0
        assert t1 > 0.0 and t1 < 1.0
        assert t2 > 0.0 and t2 < 1.0
        return t1, t2

    def set_normalized_pose(self, t1, t2):
        t1 = scale(0.0, 1.0, MIN_THETA, MAX_THETA, t1)
        t2 = scale(0.0, 1.0, MIN_THETA, MAX_THETA, t2)
        # check if the values are between MIN_THETA and MAX_THETA
        assert t1 > MIN_THETA and t1 < MAX_THETA
        assert t2 > MIN_THETA and t2 < MAX_THETA
        # if they are, set joints to the values
        self.t1 = t1
        self.t2 = t2


    def error(self, target):
        # returns the euclidian distance between the endeffector and the target
        return (self.endeffector() - target).r