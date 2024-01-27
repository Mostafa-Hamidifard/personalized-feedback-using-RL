import numpy as np
from matplotlib import pyplot as plt

time = 0

DIM = 240


class Skin():
    def __init__(self):
        self.a = 0 #modify
        self.b = 0 #modify
        self.counter = 0
        self.delay = 5
    
    def __call__(self, inp):
        if self.counter < self.delay:
            self.counter += 1
        else:
            self.counter = 0
            return self.a * np.exp(self.b * inp) #modify


class Brain():
    def __init__(self):
        
        self.counter = 0
        self.delay = 5
    
    def __call__(self, inp):
        if self.counter < self.delay:
            self.counter += 1
        else:
            self.counter = 0
            pass #modify


class EMG_Model():
    def __init__(self):
        
        self.counter = 0
        self.delay = 5
    
    def __call__(self, inp):
        if self.counter < self.delay:
            self.counter += 1
        else:
            self.counter = 0
            return inp


class Human():
    def __init__(self):
        self.skin = Skin()
        self.brain = Brain()
        self.emg = EMG_Model()
    
    def __call__(self, f, pos):
        s = self.skin(f)
        b = self.brain(s, pos)
        return self.emg(b)


class Monitor():
    def __init__(self):
        pass
    
    def __call__(self, pos, dest):
        


class Vibrator():
    def __init__(self, k):
        self.k = k
        self.counter = 0
        self.delay = 5
    
    def __call__(self, inp):
        if self.counter < self.delay:
            self.counter += 1
        else:
            self.counter = 0
            return(self.k * np.array(inp))


class Environment:
    def __init__(self):
        self.pos = np.zeros((2))
        self.dest = (np.random.rand(2)*2*DIM) - DIM
        self.human = Human()
        self.monitor = Monitor()
        self.vibrator = Vibrator(k=2)
    
    def update(self, action):
        f = self.vibrator(action)
        self.human(f, self.pos)
        self.monitor(self.pos, self.dest)