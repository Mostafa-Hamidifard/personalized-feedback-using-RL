from Environment import Environment
from Agent import Agent

from time import sleep

Episodes = 100


env = Environment()
agent = Agent()


state = env.reset()


for _ in range(Episodes):
    action = agent(state)
    state = env(action)
    sleep(0.05)