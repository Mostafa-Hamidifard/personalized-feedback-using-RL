from Environment import Environment
import numpy as np
from matplotlib import pyplot as plt

# np.random.seed(2)
# self.mapper = {"up":0,"down":1,"left":2,"right":3}


def p_controller(state,p):
    error = state["desired_position"] - state["current_position"]
    e_x = error[0]
    e_y = error[1]
    action = None
    if e_x > 0:
        if e_y >0:
            action = np.array([e_x,e_y,0,0])
            
        else:
            action = np.array([e_x,0,0,-e_y])

    else:
        if e_y >0:
            action = np.array([0,e_y,-e_x,0])
            
        else:
            action = np.array([0,0,-e_x,-e_y])
    return action

errs = []
if __name__ == '__main__':
    env = Environment(dt=0.01,max_time=10,num_vibrators=4)
 
    rewards = []
    for idx in range(500):
        reward_sum = 0
        state = env.reset()
        truncated = False
        terminated = False
        action = [40,10,0,0]
        while not(truncated or terminated):
            reward, state, terminated, truncated = env(action)
            reward_sum += reward 
            error = state["desired_position"] - state["current_position"]
            action = p_controller(state, 10)
    
        rewards.append(reward_sum)
plt.hist(rewards)
plt.title("rewards")
plt.show()
print(np.mean(rewards))