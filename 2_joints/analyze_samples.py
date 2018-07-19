import numpy as np
import matplotlib.pyplot as plt
import csv
from helper import *
from point2 import Point2

dataset_name = "dataset_20_50.0-100.0"
figsize = (5,5)
MAX_DELTA = 20
MIN_STEP  = 50.0
MAX_STEP  = 100.0

print "Analyzing {}".format(dataset_name)
print "Counting rows on file..."
row_count = sum(1 for line in open("{}.csv".format(dataset_name)))
print row_count

#GRAPHS I WANT
T1_DISTRIBUTION   = True
T2_DISTRIBUTION   = True
DX_DISTRIBUTION   = True
DY_DISTRIBUTION   = True
DT1_DISTRIBUTION  = True
DT2_DISTRIBUTION  = True
STEP_DISTRIBUTION = True

if T1_DISTRIBUTION:
    t1_x = list(np.linspace(-np.pi, np.pi, 100, endpoint=True))
    del(t1_x[0])
    t1_y  = [0 for i in t1_x]

if T2_DISTRIBUTION:
    t2_x = list(np.linspace(-np.pi, np.pi, 100, endpoint=True))
    del(t2_x[0])
    t2_y  = [0 for i in t2_x]

if DX_DISTRIBUTION:
    dx_x = list(np.linspace(-MAX_STEP, MAX_STEP, 100, endpoint=True))
    del(dx_x[0])
    dx_y  = [0 for i in dx_x]

if DY_DISTRIBUTION:
    dy_x = list(np.linspace(-MAX_STEP, MAX_STEP, 100, endpoint=True))
    del(dy_x[0])
    dy_y  = [0 for i in dy_x]

if DT1_DISTRIBUTION:
    dt1_x = list(np.linspace(np.radians(-MAX_DELTA), np.radians(MAX_DELTA), 100, endpoint=True))
    del(dt1_x[0])
    dt1_y = [0 for i in dt1_x]

if DT2_DISTRIBUTION:
    dt2_x = list(np.linspace(np.radians(-MAX_DELTA), np.radians(MAX_DELTA), 100, endpoint=True))
    del(dt2_x[0])
    dt2_y = [0 for i in dt2_x]

if STEP_DISTRIBUTION:
    step_x = list(np.linspace(MIN_STEP, MAX_STEP, 100, endpoint=True))
    del(step_x[0])
    step_y = [0 for i in step_x]

samples_checked = 0

print "Opening file..."
with open("{}.csv".format(dataset_name), 'r') as csvfile:
    reader = csv.reader(csvfile)
    for row in reader:
        # check t1
        if T1_DISTRIBUTION:
            for i, interval in enumerate(t1_x):
                y = scale(0.,1.,-np.pi, np.pi, float(row[0]))
                if y < interval:
                    t1_y[i] += 1
                    break
        # check t2
        if T2_DISTRIBUTION:
            for i, interval in enumerate(t2_x):
                y = scale(0.,1.,-np.pi, np.pi, float(row[1]))
                if y < interval:
                    t2_y[i] += 1
                    break
        # check dx
        if DX_DISTRIBUTION:
            for i, interval in enumerate(dx_x):
                y = scale(0.,1.,-MAX_STEP, MAX_STEP, float(row[2]))
                if y < interval:
                    dx_y[i] += 1
                    break
        # check dy
        if DY_DISTRIBUTION:
            for i, interval in enumerate(dy_x):
                y = scale(0.,1.,-MAX_STEP, MAX_STEP, float(row[3]))
                if y < interval:
                    dy_y[i] += 1
                    break
        # check dt1
        if DT1_DISTRIBUTION:
            for i, interval in enumerate(dt1_x):
                y = scale(0.,1.,np.radians(-MAX_DELTA), np.radians(MAX_DELTA), float(row[4]))
                if y < interval:
                    dt1_y[i] += 1
                    break
        # check dt2
        if DT2_DISTRIBUTION:
            for i, interval in enumerate(dt2_x):
                y = scale(0.,1.,np.radians(-MAX_DELTA), np.radians(MAX_DELTA), float(row[5]))
                if y < interval:
                    dt2_y[i] += 1
                    break
        # check step
        if STEP_DISTRIBUTION:
            for i, interval in enumerate(step_x):
                dx = scale(0.,1.,-MAX_STEP, MAX_STEP, float(row[2]))
                dy = scale(0.,1.,-MAX_STEP, MAX_STEP, float(row[3]))
                p = Point2(dx, dy)
                y = p.r
                if y < interval:
                    step_y[i] += 1
                    break
        samples_checked += 1
        if samples_checked % 10000 == 0:
            print "Samples checked: {}/{}".format(samples_checked, row_count)
        # if samples_checked > 50000:
        #     break

if T1_DISTRIBUTION:
    print t1_y
    plt.figure(figsize=figsize)
    plt.plot(t1_x, t1_y)
    plt.legend([r'$\theta 1$'])
    # plt.show()
    plt.savefig("graphs/{}_t1.png".format(dataset_name))

if T2_DISTRIBUTION:
    print t2_y
    plt.figure(figsize=figsize)
    plt.plot(t2_x, t2_y)
    plt.legend([r'$\theta 2$'])
    plt.savefig("graphs/{}_t2.png".format(dataset_name))

if DX_DISTRIBUTION:
    print dx_y
    plt.figure(figsize=figsize)
    plt.plot(dx_x, dx_y)
    plt.legend([r'$\Delta x$'])
    plt.savefig("graphs/{}_dx.png".format(dataset_name))

if DY_DISTRIBUTION:
    print dy_y
    plt.figure(figsize=figsize)
    plt.plot(dy_x, dy_y)
    plt.legend([r'$\Delta y$'])
    plt.savefig("graphs/{}_dy.png".format(dataset_name))

if DT1_DISTRIBUTION:
    print dt1_y
    plt.figure(figsize=figsize)
    plt.plot(dt1_x, dt1_y)
    plt.legend([r'$\Delta \theta 1$'])
    plt.savefig("graphs/{}_dt1.png".format(dataset_name))

if DT2_DISTRIBUTION:
    print dt2_y
    plt.figure(figsize=figsize)
    plt.plot(dt2_x, dt2_y)
    plt.legend([r'$\Delta \theta 2$'])
    plt.savefig("graphs/{}_dt2.png".format(dataset_name))

if STEP_DISTRIBUTION:
    print step_y
    plt.figure(figsize=figsize)
    plt.plot(step_x, step_y)
    plt.legend([r'$Step$'])
    plt.savefig("graphs/{}_step.png".format(dataset_name))




# t2_x = list(np.linspace(-np.pi, np.pi, 100, endpoint=True))
# dx_x = list(np.linspace(-50., 50., 100, endpoint=True))
# dy_x = list(np.linspace(-50., 50., 100, endpoint=True))
# dt1_x = list(np.linspace(np.radians(-15), np.radians(15), 100, endpoint=True))
# dt2_x = list(np.linspace(np.radians(-15), np.radians(15), 100, endpoint=True))

