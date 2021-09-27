import aicrowd_gym
import nle
from gym.wrappers import TimeLimit
from nethack_raph.rl_wrapper import RLWrapper


def create_env(character='@'):
    """This is the environment that will be assessed by AIcrowd."""
    return aicrowd_gym.make("NetHackChallenge-v0", character=character)


def addtimelimitwrapper_fn(character='@', verbose=False):
    """
    An example of how to add wrappers to the nethack_make_fn
    Should return a gym env which wraps the nethack gym env
    """
    env = create_env(character=character)
    env = TimeLimit(env, max_episode_steps=10_000_000)
    env = RLWrapper(env, verbose=verbose)
    return env
