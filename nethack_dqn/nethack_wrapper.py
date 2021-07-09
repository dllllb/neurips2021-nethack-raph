import gym
import nle


class NethackWrapper(gym.Wrapper):
    def __init__(self, env):
        super().__init__(env)
        self.action_space = gym.spaces.Discrete(4)
        self.observation_space = gym.spaces.Box(low=0, high=255, shape=(21, 79), dtype=float)

    def reset(self, **kwargs):
        return self._observation(self.env.reset(**kwargs))

    def step(self, action):
        state, reward, done, info = self.env.step(action)
        return self._observation(state), reward, done, info

    def _observation(self, obs):
        return obs['chars']


def make_env():
    env = NethackWrapper(gym.make('NetHackChallenge-v0', savedir=None))
    return env
