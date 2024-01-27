import numpy as np

class Agent():
    def __init__(self):
        pass
    
    def __call__(self, state):
        
        action = np.random.rand(2) #modify
        
        return action