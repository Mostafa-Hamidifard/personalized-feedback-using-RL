from Environment import Environment
from Agent import Actor, Critic
import numpy as np
from matplotlib import pyplot as plt


def actor_critic(env, actor, critic, gamma, num_Episodes):
    rewards = []
    for i in range(num_Episodes):
        state = env.reset()
        terminated = False
        truncated = False
        total_reward = 0
        
        I = 1
        while not(terminated or truncated):
            action = actor(state)
            reward, next_state, terminated, truncated = env(action)
            total_reward += reward
            if terminated:
                delta = reward - critic.value(state)
            else:
                delta = reward + gamma*critic.value(next_state) - critic.value(state)
            critic.update(delta, state)
            actor.update(I, delta, state, action)
            I *= gamma
            state = next_state
    
        rewards.append(total_reward)
        if i % 100 == 0:
            print(f'Episode {i}\tAverage Score: {sum(rewards)/len(rewards)}')
    
    return np.array(rewards)


def plot(rewards):
    ma = np.convolve(rewards, np.ones(50)/50, 'valid')
    fig, ax = plt.subplots(figsize=(10,5))
    ax.plot(ma)
    ax.set_ylabel('Rewards')
    ax.set_xlabel('Episodes')


if __name__ == '__main__':
    env = Environment()
    actor = Actor(alpha=1e-20)
    critic = Critic(alpha=1e-17)
    gamma = 0.99
    num_Episodes = 1000
    
    rewards = actor_critic(env, actor, critic, gamma, num_Episodes)
    plot(rewards)