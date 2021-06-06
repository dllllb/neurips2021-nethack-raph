from gym.wrappers import TimeLimit

from envs.nethack_make_function import nethack_make_fn

def addtimelimitwrapper_fn():
    """
    An example of how to add wrappers to the nethack_make_fn
    Should return a gym env which wraps the nethack gym env
    """
    env = nethack_make_fn()
    env = TimeLimit(env, max_episode_steps=10_000_000)
    return env