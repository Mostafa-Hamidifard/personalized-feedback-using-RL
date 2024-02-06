from Environment import Environment
from Agent import Agent
import numpy as np

num_Episodes = 5


env = Environment()
agent = Agent()


# state = env.reset()





reward_list = np.zeros((num_Episodes,))
for ep_idx in range(num_Episodes):
    print(ep_idx)
    state = env.reset()
    terminated = False
    truncated = False
    while not(terminated or truncated):
        action = agent(state)
        reward,state,terminated,truncated = env(action)
        reward_list[ep_idx] += reward  
        
        # np.append(reward_list, reward)
        # print(f"reward: {reward} , terminated: {terminated} , teruncated: {truncated}")
        # print(state['current_position'])
