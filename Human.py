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
            self.counter = 0
            self.delay = 0
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
            self.delay = 4
            self.computed_velocity = np.zeros((2,))
        
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

        def __call__(self, stimulus,angles):
            if self.counter < self.delay:
                self.counter += 1
            else:
                self.counter = 0
                percieved_error = self._calculate_percieved_error(stimulus,angles)
                self.computed_velocity = percieved_error
                
            return self.computed_velocity
    
    class EMG_Model():
        def __init__(self,delta,emg_amp_max,cross_max_ratio=0.1):
            
            self.emg_amp_max = emg_amp_max
            cross_max = cross_max_ratio * self.emg_amp_max
            self.alpha = cross_max / np.log(self.emg_amp_max + 1)
            
            self.delta = delta 
            self.counter = 0
            self.delay = 0
            self.u = np.zeros((4,))
            self.mapper = {"up":0,"down":1,"left":2,"right":3}
            
        def _u2emg(self,u_list):
            t = self.counter * self.delta
            w0 = 2*3.14*200;
            emg_list = np.zeros_like(u_list)
            for i,u in enumerate(u_list):  
                n1 = 0.1 * np.random.randn() # these paramters should get adapted
                n2 = 5 * np.random.randn()
                n3 = 0.05 * np.random.randn()
                n4 = 5  * np.random.randn()
                emg_list[i] = (u+n1)*np.sin( (w0+n2) * t + n4) + n3
                

        """BE aware that it shouldnt get delayed"""
        def __call__(self, intention):
            self.counter += 1
            
            v_x = intention[0]
            v_y = intention[1]
            
            if v_x >= 0:
                self.u[self.mapper["right"]] = min(v_x,self.emg_amp_max)
                self.u[self.mapper["left"]] = self.alpha * np.log(self.u[self.mapper["right"]] + 1)
            else:
                self.u[self.mapper["left"]] = min(-v_x,self.emg_amp_max)
                self.u[self.mapper["right"]] = self.alpha * np.log(self.u[self.mapper["left"]] + 1)
            
            if v_y >=0:
                self.u[self.mapper["up"]] = min(v_y,self.emg_amp_max)
                self.u[self.mapper["down"]] = self.alpha * np.log(self.u[self.mapper["up"]] + 1)
            else:
                self.u[self.mapper["down"]] = min(-v_y,self.emg_amp_max)
                self.u[self.mapper["up"]] = self.alpha * np.log(self.u[self.mapper["down"]] + 1)
            
            return {"modeled_emg": self._u2emg(self.u),"original": self.u}    
            
                

if __name__ == "__main__":
    human = Human(4)
    for i in range(100):
        pass
