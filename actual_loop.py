import serial.tools.list_ports
import numpy as np
import pygame
import time


class Environment:
    def __init__(self):
        pygame.init()
        self.window = pygame.display.set_mode((720, 600))
        self.pos = np.random.rand(2) * 512
        self.dest = np.random.rand(2) * 512
        self.distance_threshold = 30
        self.start_time = time.time()
        self.trial = 1
        self.terminated = False
        self.truncated = False
    
    def step(self, v):
        self.update_pos(v)
        if self.update_screen():
            return -np.ones((2,2)), -1, -1, -1
        self.check_done()
        self.calc_reward()
        return np.array((self.pos , self.dest)), self.reward, self.terminated, self.truncated
    
    def update_pos(self, v):
        self.pos += v * window/1000
        self.pos = np.clip(self.pos, 0, 512)
    
    def update_screen(self):
        self.window.fill((255, 255, 255))
        pygame.draw.circle(self.window, (0, 255, 0), self.pos.astype(int), 10)
        pygame.draw.circle(self.window, (255, 0, 0), self.dest.astype(int), 10)
        pygame.draw.rect(self.window, (0, 255, 255), [600, 0, 500, 90], 2)
        pygame.draw.rect(self.window, (255, 255, 0), [0, 0, 520, 520], 2)
        font = pygame.font.Font(None, 36)
        text = font.render(f"Trials: {self.trial}", True, (0, 0, 0))
        self.window.blit(text, (610, 10))
        text_timer = font.render(
            f"Time: {int(time.time() - self.start_time)}s", True, (0, 0, 0)
        )
        self.window.blit(text_timer, (610, 60))
        pygame.display.update()
        event = pygame.event.wait(1)
        if event.type == pygame.QUIT:
            pygame.quit()
            return True
        return False

    def check_done(self):
        if np.linalg.norm(self.pos - self.dest) < self.distance_threshold:
            self.terminated = True
            self.trial += 1
            
        if int(time.time() - self.start_time) > 10:
            self.truncated = True
            self.trial += 1

    def calc_reward(self):
        if(self.terminated):
            self.reward = 0.1 * np.exp(-np.linalg.norm(self.pos - self.dest))      
        else:
            self.reward = -1

    def reset(self):
        self.pos = np.random.rand(2) * 512
        self.dest = np.random.rand(2) * 512
        self.start_time = time.time()
        self.terminated = False
        self.truncated = False
        


class EMG:
    def __init__(self, window):
        self.window = window
        self.channel = [[] for _ in range(4)]
        
    def readLine(self, line):
        num = line.split(',')
        for i in range(4):
            self.channel[i].append(int(num[i]))

    def interpret(self):
        amp = np.array(self.channel).mean(axis=1)
        x = amp[0] - amp[1]
        y = amp[2] - amp[3]
        
        if abs(x) < 50:
            x = 0
        # if x < 0:
        x /= 3
        
        if abs(y) < 50:
            y = 0
        y /= 2
        
        return np.array([x,y])


def run():
    running = True
    while running:
        try:
            emg = EMG(window)
            for _ in range(window):
                packet = serialInst.readline()
                inp = str(packet.decode('utf').rstrip('\n'))
                emg.readLine(inp)
            v = emg.interpret()
            
            observation, reward, terminated, truncated = env.step(v)
            if terminated or truncated:
                env.reset()
            if (observation == -np.ones((2,2))).all():
                running = False
            # action = Agent(observation, reward)
            action = "0,0,0,0,0,0,0,0,"
            serialInst.write(action.encode('utf-8'))
        except:
            pass


#main code
serialInst = serial.Serial('COM6', 115200)
env = Environment()
window = 100

run()

off = '0,0,0,0,0,0,0,0,'
serialInst.write(off.encode('utf-8'))
serialInst.close()