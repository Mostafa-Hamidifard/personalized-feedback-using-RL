import numpy as np


class Human():
    def __init__(self,num_vibrators,angle=None):
        self.skin = self.Skin(num_vibrators,angle)
        self.brain = self.Brain()
        self.emg = self.EMG_Model()
    
    def __call__(self, f, pos):
        stimulus = self.skin(f)
        intention = self.brain(stimulus,self.skin.angles, pos)
        return self.emg(intention)



    class Skin():
        """angles is a tuple which contains the angles corrosponding to the vibrator positions computed CCW
        from right arm.
        """
        def __init__(self,num_vibrators,angles=None,options = None):            
            if options != None:
                pass            
            
            self.num_vibrators = num_vibrators
            self.angles = angles

            if self.angles == None:
                self.angles = [i / self.num_vibrators * 2*np.pi for i in range(self.num_vibrators)]

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
            self.delay = 20
            self.target_pos = np.zeros((2,))
        
        """
        It is assumed that vibrations are distributed around human body,
        so the percieved error in each direction is proportional to intensity on
        that direction. total percieved error is the sum of percieved error from
        each vibrator.
        """
        def _calculate_percieved_error(self,stimulus,angles):
            n = len(stimulus)
            percieved_error = np.zeros((2,))
            for idx in range(n):
                angle = angles[idx]
                vec = np.array([np.cos(angle) , np.sin(angle)])
                percieved_error = percieved_error + stimulus[idx] * vec
            return percieved_error                

        def __call__(self, stimulus,angles, pos):
            if self.counter < self.delay:
                self.counter += 1
            else:
                self.counter = 0
                percieved_error = self._calculate_percieved_error(stimulus,angles)
                self.target_pos = pos + percieved_error
                
            return self.target_pos
    
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

if __name__ == "__main__":
    human = Human(4)
    for i in range(100):
        print(i)
        print(human.brain([1,0,1,2*i],human.skin.angles,0))
