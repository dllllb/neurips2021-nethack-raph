import numpy as np
from tqdm import trange
from collections.abc import Iterable
from envs.nethack_make_function import nethack_make_fn


class NetHackChallengeBatchedEnv:
    def __init__(self, env_make_fn, num_envs=1):
        """
        Creates multiple copies of the NetHackChallenge environment
        """

        self.num_envs = num_envs
        self.envs = [env_make_fn() for _ in range(self.num_envs)]

        self.action_space = self.envs[0].action_space
        self.observation_space = self.envs[0].observation_space
        self.reward_range = self.envs[0].reward_range

    def step(self, actions):
        """
        Applies each action to each env in the same order as self.envs
        Actions should be iterable and have the same length as self.envs
        Returns lists of obsevations, rewards, dones, infos
        """
        assert isinstance(
            actions, Iterable), f"actions with type {type(actions)} is not iterable"
        assert len(
            actions) == self.num_envs, f"actions has length {len(actions)} which different from num_envs"

        observations, rewards, dones, infos = [], [], [], []
        for env, a in zip(self.envs, actions):
            observation, reward, done, info = env.step(a)
            if done:
                observation = env.reset()
            observations.append(observation)
            rewards.append(reward)
            dones.append(done)
            infos.append(info)

        return observations, rewards, dones, infos

    def reset(self):
        """
        Resets all the environments in self.envs
        """
        observations = [env.reset() for env in self.envs]
        return observations

    def single_env_reset(self, index):
        """
        Resets the env at the index location
        """
        observation = self.envs[index].reset()
        return observation
    
    def single_env_step(self, index, action):
        """
        Resets the env at the index location
        """
        observation, reward, done, info = self.envs[index].step(action)
        return observation, reward, done, info

if __name__ == '__main__':
    num_envs = 4
    batched_env = NetHackChallengeBatchedEnv(env_make_fn=nethack_make_fn, num_envs=num_envs)
    observations = batched_env.reset()
    num_actions = batched_env.action_space.n
    for _ in trange(10000000000000):
        actions = np.random.randint(num_actions, size=num_envs)
        observations, rewards, dones, infos = batched_env.step(actions)
        for done_idx in np.where(dones)[0]:
            observations[done_idx] = batched_env.single_env_reset(done_idx)
