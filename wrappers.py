from gym.wrappers import TimeLimit

from nethack_baselines.utils.nethack_env_creation import nethack_make_fn

def addtimelimitwrapper_fn():
    """
    An example of how to add wrappers to the nethack_make_fn
    Should return a gym env which wraps the nethack gym env
    """
    env = nethack_make_fn()
    env = TimeLimit(env, max_episode_steps=10_000_0000)
    return env