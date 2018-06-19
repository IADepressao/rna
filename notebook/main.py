# imports
import numpy as np
import random
import io

class RNA():
    def __init__(self, bias=False, momentum=False, learning_rate=0.5, sigmoid=True):
        self.bias = bias
        self.momentum = momentum
        self.learning_rate = learning_rate
        self.sigmoid = sigmoid

    def sigmoid(self, soma):
        return 1 / (1 + np.exp(-soma))

    def sigmoidDerivate(self, sig):
        return sig * (1 - sig)

    def treinar(self):
        pass

    def testar(self):
        pass

class Data():
    def __init__(self):
        self.header = 0
        self.data = 0
        self.output = 0
        self.train = 0
        self.test = 0
        self.train_out = 0
        self.test_out = 0

    def ready(self, path='dataset/fertility.csv', train_percent=80):
        data = np.loadtxt(path, dtype=str, delimiter=',')
        self.header, data = np.array_split(data, [1])
        data, self.output = np.array_split(data, [9], axis=1)
        self.data = data.astype(np.float)

        self.train = self.data[:train_percent]
        self.test = self.data[train_percent:]
        self.train_out = self.output[:train_percent]
        self.test_out = self.output[train_percent:]
