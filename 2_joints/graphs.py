import numpy as np
import matplotlib.pyplot as plt
import csv


plt.figure(figsize=(8,8))

# COMPARE NET AND JACOBIAN PERFORMANCE
netx = []
nety = []
with open("reports/net_control20180714_154336.csv", 'r') as csvfile:
    reader = csv.reader(csvfile)
    for row in reader:
        x = round(float(row[0]), 1)
        # if x < 16.1:
        netx.append(x)
        nety.append(float(row[1]))

plt.plot(netx, nety)
# plt.legend(["net"])

jacx = []
jacy = []
with open("reports/jacobian_control_15_20-50.csv", 'r') as csvfile:
    reader = csv.reader(csvfile)
    for row in reader:
        x = round(float(row[0]), 1)
        # if x < 16.1:
        jacx.append(x)
        jacy.append(float(row[1]))

plt.plot(jacx, jacy)
plt.legend(["net", "jacobian"])
plt.savefig("net_vs_jac_15_20-50.png")
# plt.show()