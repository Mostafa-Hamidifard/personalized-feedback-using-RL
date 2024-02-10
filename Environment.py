from Human import Human
from EMG_Interpretation import EMG_Interpretation
import numpy as np
# import pygame
# import Threading
# import sys

DIM = 512
X = 0
Y = 1

class Environment:
    def __init__(self,dt=0.01,max_time=10,num_vibrators=8):
        self.dt = dt
        self.pos = np.zeros((2))
        self.dest = np.random.rand(2)*DIM  # desired position
        
        self.human = Human(num_vibrators,dt)
        self.vibrator = self.Vibrator(k=1)
        self.dynamic = self.Dynamical_model(self.pos, dt)
        self.reward = self.Reward(dt,max_time)
        
        # self.monitor = self.Monitor()
        
    def __call__(self, action):
        f = self.vibrator(action)
        emg = self.human(f)

        # if not emg:
        #     emg = np.random.rand(2) * DIM # new_pos
        
        v  = EMG_Interpretation(emg) 
        self.pos = self.dynamic.update(v)
        
        reward, terminated, truncated = self.reward.calc_reward(self.pos, self.dest)
        # self.monitor(self.pos, self.dest)
        state = {"desired_position":self.dest , "current_position":self.pos}
        
        return reward, state, terminated, truncated
    
    def reset(self):
        self.pos = np.zeros((2))
        self.dest = np.random.rand(2)*DIM # desired position
        self.dynamic.reset(self.pos)
        self.reward.reset()
        self.human.reset()
        state = {"desired_position":self.dest , "current_position":self.pos}
        return state
        
    class Dynamical_model:
        def __init__(self,initial_position,dt):
            self.p = initial_position.reshape((-1,))
            self.dt = dt
            
        def update(self,input_u):
            self.p = self.p + self.dt * input_u
            return self.p
            
        def get_position(self):
            return self.p
        
        def reset(self,initial_position):
            self.p = initial_position.reshape((-1,))
    
    class Reward:
        def __init__(self,dt,max_time,hold_time=2,distance_threshold=10):
            self.dt = dt
            self.distance_threshold = distance_threshold
            self.max_step = max_time //self.dt
            self.hold_time = hold_time
            self.truncate_counter = 0
            self.terminate_counter = 0
            self.k_ter = 1000
            self.alpha = np.log(10)/distance_threshold
            self.k_teru = 1
            self.r_d = -1 
            
        def check_done(self,distance):
            terminated = False
            truncated = False
            if np.linalg.norm(distance)<self.distance_threshold:
                self.terminate_counter += 1
            else:
                self.terminate_counter = 0
                
            if self.terminate_counter >= (self.hold_time//self.dt):
                terminated = True
            
            if self.truncate_counter >= self.max_step:
                truncated = True
                
            return terminated,truncated
        
        def reset(self):
            self.truncate_counter = 0
            self.terminate_counter = 0
                

        def calc_reward(self,pos,dest):
            self.truncate_counter += 1
            
            distance = pos - dest
            
            terminated , truncated = self.check_done(distance)
            reward = 0 
            if(terminated):
                reward=  self.k_ter * np.exp(-1 * self.alpha * np.linalg.norm(distance))      
            
            elif (truncated):
                reward = -self.k_teru * np.linalg.norm(distance)  
            else:
                reward =  self.r_d
            return reward, terminated, truncated
    
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
