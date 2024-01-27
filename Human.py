import numpy as np


class Human():
    def __init__(self):
        self.skin = self.Skin()
        self.brain = self.Brain()
        self.emg = self.EMG_Model()
    
    def __call__(self, f, pos):
        stimulus = self.skin(f)
        intention = self.brain(stimulus, pos)
        return self.emg(intention)



    class Skin():
        def __init__(self,num_vibrators,interDistance,options = None):            
            if options != None:
                pass            

            self.num_vibrators = num_vibrators
            self.interDistance = interDistance
            # The question here is that why these numbers?
            self.a = np.random.uniform(1,8,size=(num_vibrators,))
            self.b = np.random.uniform(0.4,2,size=(num_vibrators,)) #modify

        def __call__(self, inp):
            if self.counter < self.delay:
                self.counter += 1
            else:
                self.counter = 0
                # be aware that inp must convert to a 1d vector
                inp = inp.reshape((-1,))
                return self.a * np.exp(self.b * inp) 
                return self.a * np.exp(self.b * inp) #modify
    
    
    
    class Brain():
        def __init__(self):
            
            self.counter = 0
            self.delay = 5
        
        def __call__(self, stimulus, pos):
            if self.counter < self.delay:
                self.counter += 1
            else:
                self.counter = 0
                pass #modify
    
    
    class EMG_Model():
        def __init__(self):
            
            self.counter = 0
            self.delay = 5
        
        def __call__(self, intention):
            if self.counter < self.delay:
                self.counter += 1
            else:
                self.counter = 0
                return intention


