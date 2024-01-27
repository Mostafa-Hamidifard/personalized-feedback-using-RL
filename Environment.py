import Human
import numpy as np
from matplotlib import pyplot as plt

DIM = 240
X = 0
Y = 1

class Environment:
    def __init__(self):
        self.pos = np.zeros((2))
        self.dest = (np.random.rand(2)*2*DIM) - DIM
        self.human = Human.Human()
        self.monitor = self.Monitor()
        self.vibrator = self.Vibrator(k=2)
    
    def update(self, action):
        f = self.vibrator(action)
        self.human(f, self.pos)
        self.monitor(self.pos, self.dest)


    class Monitor():
        def __init__(self):
            pass
        
        def __call__(self, pos, dest):
            self.fig, self.ax = plt.subplots(figsize=(10,5))
            self.ax.cla()
            self.ax.scatter(pos[X], pos[Y], marker='o', color='b')
            self.ax.scatter(dest[X], dest[Y], marker='o', color='r')
            plt.xlim((-DIM,DIM))
            plt.ylim((-DIM,DIM))
            self.ax.set_xlabel('X')
            self.ax.set_ylabel('Y')
            self.ax.set_title('Map')
    
    
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
