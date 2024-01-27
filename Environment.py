import Human
import EMG_Interpretation
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
    
    def __call__(self, action):
        f = self.vibrator(action)
        emg = self.human(f, self.pos)
        self.pos = EMG_Interpretation.EMG_Interpretation(emg)
        self.monitor(self.pos, self.dest)
        return self.pos

    class Monitor():
        def __init__(self):
            pass
        
        def __call__(self, pos, dest):
            fig, ax = plt.subplots(figsize=(10,5))

            ax.scatter(dest[X], dest[Y], marker='o', color='r')
            ax.scatter(pos[X], pos[Y], marker='o', color='b')
            plt.xlim((-DIM,DIM))
            plt.ylim((-DIM,DIM))
            ax.set_xlabel('X')
            ax.set_ylabel('Y')
            ax.set_title('Map')
    
    
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
