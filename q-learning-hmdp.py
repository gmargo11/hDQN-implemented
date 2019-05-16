import numpy as np
import random
import gym
import matplotlib

from collections import defaultdict
from envs.hmdp import StochastichMDPEnv as hMDP
import utils.plotting as plotting


class QLearningAgent():

    def __init__(self, env = hMDP(), num_episodes = 20000, \
                gamma = 0.9, alpha = 0.6, batch_size = 1, epsilon_anneal = 1/2000):
    self.env = env
    self.num_episodes = num_episodes
    self.gamma = gamma
    self.alpha = alpha
    self.batch_size = batch_size
    self.epsilon_anneal = epsilon_anneal



    def epsGreedy(self, state, B, eps, Q):
        action_probabilities = np.ones_like(Q[state]) * epsilon / len(Q[state])
        best_action = np.argmax(Q[state])
        action_probabilities[best_action] += (1.0 - eps)
        action = np.random.choice(np.arange(len(action_probabilities)), p = action_probabilities)
        return action

    def QValueUpdate(self, Q, D):
        batch_size = 1
        gamma = 0.9
        alpha = 0.6
        mini_batch = random.sample(D, batch_size)

        for s, action, f, s_next, done in mini_batch:
            target = f
            if not done:
                best_next_action = np.argmax(Q[s_next])
                target = f + gamma * Q[s_next][best_next_action]
            delta = target - Q[s][action]
            Q[s][action] += alpha * delta

        return Q

    def learn(self):

        stats = plotting.EpisodeStats( 
                episode_lengths = np.zeros(self.num_episodes), 
                episode_rewards = np.zeros(self.num_episodes)) 

        #env = WindyGridworldEnv()
        env = hMDP()

        D = None
        Q = defaultdict(lambda: np.zeros(self.env.action_space.n))
        A = self.env.action_space

        epsilon = 1.0

        for i in range(self.num_episodes):
            if i % 1000 == 0:
                    print('Episode ', i)
                    print(epsilon)
            s = self.env.reset()
            done = False
            t = 0
            while not done:
                action = self.epsGreedy(s, A, epsilon, Q)
                s_next, f, done, _ = self.env.step(action)
                stats.episode_rewards[i] += f
                stats.episode_lengths[i] = t

                D = [(s, action, f, s_next, done)]
                Q = self.QValueUpdate(Q, D)
                s = s_next
                t += 1
            epsilon = max(epsilon - 1 / 12000, 0.1)

        return stats
        #plotting.plot_episode_stats(stats, smoothing_window=1000)

if __name__ == "__main__":
    agent = hierarchicalQLearningAgent(env=hMDP())
    stats = agent.learn()
    plotting.plot_episode_stats(stats, smoothing_window=1000)





