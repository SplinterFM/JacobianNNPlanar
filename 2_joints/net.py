from point2 import Point2
import numpy as np
from arm import *
from keras.models import load_model
from helper import *

class Net:
    def __init__(self, modelid, arm=Arm()):
        self.arm = arm
        model_file = "nets/model{}.h5".format(modelid)
        self.model = load_model(model_file)

    def control(self, target):
        nt1, nt2  = self.arm.get_normalized_pose()
        curr_end  = self.arm.endeffector()
        delta_pos = target - curr_end

        dx = scale(-MAX_STEP, MAX_STEP, 0.0, 1.0, delta_pos.x)
        dy = scale(-MAX_STEP, MAX_STEP, 0.0, 1.0, delta_pos.y)

        # feed the net
        net_in = np.array([nt1, nt2, dx, dy])
        net_out = self.model.predict(net_in.reshape(1,4))[0]
        dt1 = scale(0.0, 1.0, MIN_DT, MAX_DT, net_out[0])
        dt2 = scale(0.0, 1.0, MIN_DT, MAX_DT, net_out[1])
        assert dt1 >= MIN_DT and dt1 <= MAX_DT
        assert dt2 >= MIN_DT and dt2 <= MAX_DT

        self.arm.move(dt1, dt2)
