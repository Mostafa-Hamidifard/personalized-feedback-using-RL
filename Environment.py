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
    def __init__(self,dt=0.0001):
        self.pos = np.zeros((2))
        self.dest = (np.random.rand(2)*2*DIM) - DIM
        
  

        self.human = Human()
        self.monitor = self.Monitor()
        self.vibrator = self.Vibrator(k=2)
    
    
    
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

    class Monitor():
        def __init__(self,render_mode=None):
            self.render_mode = render_mode
            self.is_window_displaying = False
            self.p_current = np.array([0,0])
            self.p_desired = np.array([0,0])
            self.circle_radius = 0
            self.desired_rect = None
            self.current_rect = None
            self.show_desired = True
            
        def turn_off_monitor(self):
            if self.is_window_displaying:
                pygame.quit()
                self.is_window_displaying = False
        
        def turn_on_monitor(self,width=480,height=480):
            if self.render_mode != 'human':
                print("render_mode is not set to <human>.")
                return 0
            pygame.init()
            self.window = pygame.display.set_mode((width,height))
            self.is_window_displaying = True
            
            self.circle_radius = width//20
            
            def draw_thread():
                p_current = self.p_current
                p_desired = self.p_desired
                if self.show_desired == True:    
                    self.desired_rect =  pygame.draw.circle(self.window, (255,0,0), p_desired[0],p_desired[1], self.circle_radius)
                self.current_rect = pygame.draw.circle(self.window, (0,0,255), p_current[0],p_current[1], self.circle_radius)
                
            def runnimg_loop():
                running = True
                while self.is_window_displaying and running:
                    for event in pygame.event.get():
                        if event.type == pygame.QUIT:
                            running = False  
                            # sys.exit("window was closed")
                self.turn_off_monitor()
            
                
        def __call__(self, pos, dest):
            pass
    
    
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
