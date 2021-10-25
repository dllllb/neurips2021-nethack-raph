import aicrowd_gym
import nle
from gym.wrappers import TimeLimit
import gym
from nethack_raph.rl_wrapper import RLWrapper


def create_env(character='@'):
    """This is the environment that will be assessed by AIcrowd."""
    return aicrowd_gym.make("NetHackChallenge-v0", character=character)


def addtimelimitwrapper_fn(character='@'):
    """
    An example of how to add wrappers to the nethack_make_fn
    Should return a gym env which wraps the nethack gym env
    """
    env = create_env(character=character)
    env = TimeLimit(env, max_episode_steps=10_000_000)
    return env

def addtimelimitwrapper_fn_custom(character='@', verbose=False):
    env = addtimelimitwrapper_fn(character)
    env = InfoWrapper(env)
    return env

def addtimelimitwrapper_fn_rl(character='@', verbose=False):
    env = addtimelimitwrapper_fn(character)
    env = RLWrapper(env, verbose=verbose)
    return env

def minihack_task(task='MiniHack-CorridorBattle-v0', character='@'):
    import minihack
    from nle.env.base import FULL_ACTIONS
    env = gym.make(task, character=character, actions=FULL_ACTIONS)
    env = InfoWrapper(env)
    return env

class InfoWrapper(gym.Wrapper):
    def __init__(self, env):
        self.env = env
        self.episode_reward = 0
        self.action_space = env.action_space

    def reset(self):
        self.episode_reward = 0
        obs = self.env.reset()
        return obs

    def step(self, action):
        obs, reward, done, info = self.env.step(action)
        self.episode_reward += reward

        if done:
            info['episode'] = {'r': self.episode_reward}
            info['role'] = '@'

        return obs, reward, done, info
