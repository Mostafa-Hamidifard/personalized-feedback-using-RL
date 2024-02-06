from Human import Human
from EMG_Interpretation import EMG_Interpretation
import numpy as np
import pygame
# import Threading
# import sys

DIM = 240
X = 0
Y = 1

class Environment:
    def __init__(self,dt=0.0001,num_vibrators=8):
        self.pos = np.zeros((2))
        self.dest = (np.random.rand(2)*2*DIM) - DIM # desired position
        
        self.human = Human(num_vibrators)
        self.vibrator = self.Vibrator(k=2)

        self.reward = self.Reward(dt,self.dest)
        self.terminated = False
        self.truncated = False

        # self.monitor = self.Monitor()
        
    
    
    def __call__(self, action):
        f = self.vibrator(action)
        emg = self.human(f, self.pos)
        
        if not emg:
            emg = np.random.rand(2) * DIM # new_pos
        
        self.pos = EMG_Interpretation(emg)
        self.monitor(self.pos, self.dest)
        return self.pos
    
    def reset(self):
        self.__init__()


    class dynamical_model:
        def __init__(self,initial_position,dt):
            
            self.p = initial_position.reshape((-1,))
            self.dt = dt
            
        def update(self,input_u):
            self.p = self.p + self.dt * input_u
            return self.p
            
        def get_position(self):
            return self.p
        
    class Reward:
        def __init__(self,dt,dest):
            self.dt = dt
            self.counter = 0
            
            self.k_r = 0.1
            self.r_d = -1 
            self.dest = dest
        def check_done(self,pos):
            while np.linalg.norm(pos-self.dest)<10:
                self.counter+=1
                if self.counter>=(2/self.dt):
                    self.terminated=True
                    break
        

        def calc_reward(self,pos):
            self.check_done()
            distance = pos - self.dest
            if(self.terminated):
                return self.k_r * np.exp(-np.linalg.norm(distance))      
            else:
                return self.r_d
    
    
    class Vibrator():
        def __init__(self, k ,delay=0):
            self.k = k
            self.counter = 0
            self.delay = delay
        
        def __call__(self, inp):
            if self.counter < self.delay:
                self.counter += 1
            else:
                self.counter = 0
                return(self.k * np.array(inp))
