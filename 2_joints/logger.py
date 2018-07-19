import numpy as np
import matplotlib.pyplot as plt
import csv


class Logger:
    def __init__(self, name):
        self.x = []
        self.y = []
        self.name = name
        csvpath = 'reports/{}.csv'.format(name)
        csvfile = open(csvpath, 'wb')
        self.csvwriter = csv.writer(csvfile)

    def add_data(self, x, y):
        self.x.append(x)
        self.y.append(y)
        self.csvwriter.writerow([x, y])

    def plot(self, xlabel, ylabel, name=-1):
        if name == -1:
            name = self.name
        plt.plot(self.x, self.y)
        plt.xlabel(xlabel)
        plt.ylabel(ylabel)
        image_path = 'reports/{}.png'.format(name)
        plt.savefig(image_path)





