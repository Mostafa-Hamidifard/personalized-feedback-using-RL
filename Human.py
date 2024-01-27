import numpy as np


class Human():
    def __init__(self):
        self.skin = self.Skin()
        self.brain = self.Brain()
        self.emg = self.EMG_Model()
    
    def __call__(self, f, pos):
        s = self.skin(f)
        b = self.brain(s, pos)
        return self.emg(b)



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


