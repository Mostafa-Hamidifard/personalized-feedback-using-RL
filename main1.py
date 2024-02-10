from Environment import Environment
import numpy as np
from matplotlib import pyplot as plt



def plot(rewards):
    ma = np.convolve(rewards, np.ones(50)/50, 'valid')
    fig, ax = plt.subplots(figsize=(10,5))
    ax.plot(ma)
    ax.set_ylabel('Rewards')
    ax.set_xlabel('Episodes')


if __name__ == '__main__':
    env = Environment(dt=0.01,max_time=10,num_vibrators=4)
    state = env.reset()
    
    action = [0,0,0,0]
    for i in range(100):
        reward, state, terminated, truncated = env(action)
        print(state)
