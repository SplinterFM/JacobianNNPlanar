from ezgame import Ezgame
from point2 import Point2
import numpy as np
import csv

from arm import *
from trajectory import Trajectory
from jacobian import JacobianControler
from net import Net
from helper import *
from logger import Logger

FPS = 100000


# APPLICATION MODES
JACOBIAN            = 0
RANDOM_POSE         = 1
GENERATE_SAMPLES    = 2
TEST_NETWORK        = 3
MODELID = "20180714_154336"

CURRENT_MODE = GENERATE_SAMPLES

class Application:
    def __init__(self):
        self.ez = Ezgame(700, 700)
        self.ez.fps = FPS
        self.loop = CURRENT_MODE

        self.arm = Arm()
        self.init()


    def init(self):
        if self.loop == JACOBIAN:
            self.ez.init(self.jacobian_loop)
            # needs a trajectory
            self.traj_step  = TRAJ_STEP_MIN
            self.trajectory = Trajectory(
                step_length=self.traj_step,
                restart=self.reset)
            self.jacobian   = JacobianControler(self.arm)
            self.errors = []
            self.plot_errors = []
            self.jacobian_logger = Logger("jacobian_control")
            # self.ez.gui = False

        elif self.loop == RANDOM_POSE:
            self.ez.init(self.random_pose_loop)
            self.arm2 = Arm()
            self.ez.fps = 2

        elif self.loop == GENERATE_SAMPLES:
            self.ez.init(self.generate_samples_loop)
            self.arm2 = Arm()
            self.ez.gui = False

            # the file has in its name the range of delta theta in degrees
            # and the maximum step valid
            filename = "dataset_{}_{}-{}.csv".format(DT_VAL, MIN_STEP, MAX_STEP)
            csvfile = open(filename, 'a')
            self.dataset_writer  = csv.writer(csvfile)
            self.sample_counter  = 0
            self.invalid_counter = 0

        elif self.loop == TEST_NETWORK:
            self.ez.init(self.test_net_loop)
            # needs a trajectory
            self.traj_step  = TRAJ_STEP_MIN
            self.trajectory = Trajectory(
                step_length=self.traj_step,
                restart=self.reset)
            modelid = MODELID
            self.net = Net(modelid, self.arm)
            self.errors = []
            self.net_logger = Logger("net_control{}".format(modelid))


    def test_net_loop(self):
        self.draw_arm(self.arm)
        self.draw_trajectory()

        # get current position
        t1  = self.arm.t1
        t2  = self.arm.t2
        ee1 = self.arm.endeffector()

        self.current_point = self.trajectory.current()
        self.net.control(self.current_point)
        self.errors.append(self.arm.error(self.current_point))
        self.draw_info()

        self.current_point = self.trajectory.next()

        self.ez.point(self.arm.endeffector(), color='blue')



    def jacobian_loop(self):
        self.draw_arm(self.arm)
        self.draw_trajectory()

        self.current_point = self.trajectory.current()
        self.jacobian.control(self.current_point)

        self.errors.append(self.arm.error(self.current_point))
        self.draw_info()

        self.current_point = self.trajectory.next()

        self.ez.point(self.arm.endeffector(), color='blue')

    def random_pose_loop(self):
        self.arm.set_random_pose()
        t1, t2 = self.arm.get_normalized_pose()
        self.arm2.set_normalized_pose(t1, t2)
        self.draw_arm(self.arm)
        self.draw_arm(self.arm2)

    def generate_samples_loop(self):
        sample = self.generate_sample()
        vector = Point2(sample[2], sample[3])
        if vector.r > MIN_STEP and vector.r < MAX_STEP:
            norm_sample = self.normalize_sample(sample)
            self.dataset_writer.writerow(norm_sample)
            self.sample_counter += 1
        else:
            self.invalid_counter += 1

        if self.sample_counter % 10000 == 0:
            print "{} samples generated in this loop.".format(self.sample_counter)
            avg = self.sample_counter/float((self.sample_counter + self.invalid_counter))
            print "{}% valid".format(avg*100.)

        if self.sample_counter >= 2000000:
            self.exit()


    def generate_sample(self):
        # generate random position
        self.arm.set_random_pose()

        #view
        # self.draw_arm(self.arm, color='blue')
        #endview

        t1, t2 = self.arm.t1, self.arm.t2
        ee1 = self.arm.endeffector()

        # generate random movement
        dt1 = normal_in_range(MIN_DT, MAX_DT)
        dt2 = normal_in_range(MIN_DT, MAX_DT)
        # dt1 = scale(0.0, 1.0, MIN_DT, MAX_DT, np.random.random())
        # dt2 = scale(0.0, 1.0, MIN_DT, MAX_DT, np.random.random())
        # move arm
        self.arm.move(dt1, dt2)
        ee2 = self.arm.endeffector()
        dee = ee2 - ee1

        #view
        # self.arm2.t1, self.arm2.t2 = self.arm.t1, self.arm.t2
        # self.draw_arm(self.arm2, color='red')
        # print [t1,t2, dee.x, dee.y, dt1, dt2], ":", ee1, " ->", ee2
        # raw_input()
        #endview

        return [t1,t2, dee.x, dee.y, dt1, dt2]

    def normalize_sample(self, sample):
        t1  = scale(MIN_THETA, MAX_THETA, 0.0, 1.0, sample[0])
        t2  = scale(MIN_THETA, MAX_THETA, 0.0, 1.0, sample[1])
        dx  = scale(-MAX_STEP, MAX_STEP, 0.0, 1.0, sample[2])
        dy  = scale(-MAX_STEP, MAX_STEP, 0.0, 1.0, sample[3])
        dt1 = scale(MIN_DT, MAX_DT, 0.0, 1.0, sample[4])
        dt2 = scale(MIN_DT, MAX_DT, 0.0, 1.0, sample[5])

        norm_sample = [t1, t2, dx, dy, dt1, dt2]
        for value in norm_sample:
            assert value >= 0.0 and value <= 1.0
        return norm_sample


    def draw_arm(self, arm, color='black'):
        p1 = Point2().polar(arm.l1, arm.t1)
        p2 = Point2().polar(arm.l2, arm.t2+arm.t1) + p1
        self.ez.line(Point2(), p1, color=color)
        self.ez.point(p1)
        self.ez.line(p1, p2, color=color)
        self.ez.point(p2)

    def draw_trajectory(self):
        self.ez.lines(self.trajectory.points)

    def draw_info(self):
        # tamanho do passo atual
        val = self.traj_step
        val_text = "Step size.....{0}".format(val)
        self.ez.text(val_text, Point2(10,10), onScreen=True)
        # passo atual
        val = self.trajectory.curr_idx()
        val_text = "Current step..{0}".format(val)
        self.ez.text(val_text, Point2(10,20), onScreen=True)
        # erro medio
        val = self.mse()
        val_text = "Avg. error....{0}".format(val)
        self.ez.text(val_text, Point2(10,30), onScreen=True)

        if self.loop == JACOBIAN:
            # temporary
            if len(self.plot_errors) > 2:
                self.ez.lines(self.plot_errors,color='blue')

    def mse(self):
        squared = [e*e for e in self.errors]
        # squared = [e for e in self.errors]
        return sum(squared)/float(len(squared))

    def run(self):
        self.ez.run()

    def reset(self):
        mse = self.mse()
        print self.traj_step, mse

        if self.loop == TEST_NETWORK:
            self.net_logger.add_data(self.traj_step, mse)
        elif self.loop == JACOBIAN:
            self.jacobian_logger.add_data(self.traj_step, mse)


        self.traj_step += TRAJ_STEP_INC
        if self.traj_step > TRAJ_STEP_MAX:
            self.exit()

        self.trajectory = Trajectory(
            step_length=self.traj_step,
            restart=self.reset)
        self.errors = []
        self.arm = Arm()

        if self.loop == JACOBIAN:
            self.jacobian.arm = self.arm
            # temporary
            self.plot_errors.append(
                Point2(self.traj_step * 10, mse*1000)
            )
        elif self.loop == TEST_NETWORK:
            self.net.arm = self.arm

    def exit(self):
        if self.loop == TEST_NETWORK:
            self.net_logger.plot("Step Size", "MSE")
        if self.loop == JACOBIAN:
            self.jacobian_logger.plot("Step Size", "MSE")
        raw_input()
        exit()


if __name__ == '__main__':
    app = Application()
    app.run()