import aicrowd_gym
import numpy as np
from tqdm import trange
from collections.abc import Iterable

class BactchedEnv:
    def __init__(self, env_make_fn, num_envs=32):
        """
        Creates multiple copies of the environment with the same env_make_fn function
        """
        self.num_envs = num_envs
        self.envs = [env_make_fn() for _ in range(self.num_envs)]
        self.num_actions = self.envs[0].action_space.n

    def batch_step(self, actions):
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

    def batch_reset(self):
        """
        Resets all the environments in self.envs
        """
        observation = [env.reset() for env in self.envs]
        return observation

    def single_env_reset(self, index):
        """
        Resets the env at the index location
        """
        observation = self.envs[index].reset()
        return observation


if __name__ == '__main__':

    def nethack_make_fn():
        return aicrowd_gym.make('NetHackChallenge-v0',
                         observation_keys=("glyphs",
                                          "chars",
                                          "colors",
                                          "specials",
                                          "blstats",
                                          "message",
                                          "tty_chars",
                                          "tty_colors",
                                          "tty_cursor",))

    num_envs = 4
    batched_env = BactchedEnv(env_make_fn=nethack_make_fn, num_envs=num_envs)
    observations = batched_env.batch_reset()
    num_actions = batched_env.envs[0].action_space.n
    for _ in trange(10000000000000):
        actions = np.random.randint(num_actions, size=num_envs)
        observations, rewards, dones, infos = batched_env.batch_step(actions)
        for done_idx in np.where(dones)[0]:
            observations[done_idx] = batched_env.single_env_reset(done_idx) 
