from point2 import Point2
import numpy as np
from arm import Arm

class JacobianControler:
    def __init__(self, arm=Arm()):
        self.arm = arm

    def control(self, target):
        curr_end  = self.arm.endeffector()
        delta_pos = target - curr_end

        iJ = 1/(self.arm.l1*self.arm.l2*np.sin(self.arm.t2)) * np.array([
        [self.arm.l2*np.cos(self.arm.t1 + self.arm.t2),
         self.arm.l2*np.sin(self.arm.t1 + self.arm.t2)],
        [-self.arm.l1*np.cos(self.arm.t1)-self.arm.l2*np.cos(self.arm.t1+self.arm.t2),
         -self.arm.l1*np.sin(self.arm.t1)-self.arm.l2*np.sin(self.arm.t1+self.arm.t2)]
        ])
        
        delta_joints = iJ.dot(np.array([delta_pos.x, delta_pos.y]))

        # self.arm.t1 += delta_joints[0]
        # self.arm.t2 += delta_joints[1]
        self.arm.move(delta_joints[0], delta_joints[1])