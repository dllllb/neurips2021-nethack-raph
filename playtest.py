import numpy as np

import nle
import aicrowd_gym
from gym.wrappers import TimeLimit

from agents.custom_agent import CustomAgent
from envs.wrappers import addtimelimitwrapper_fn


from rollout import run_batched_rollout
from envs.batched_env import BatchedEnv

from nle_toolbox.wrappers.replay import Replay, ReplayToFile


def evaluate(seed=None):

    with ReplayToFile(
        Replay(addtimelimitwrapper_fn()),
        folder='./replays',
        save_on='close,done',
    ) as env:
        # ensure seed prior to making a lambda factory
        env.seed(seed=tuple(seed))

        batched_env = BatchedEnv(env_make_fn=lambda: env, num_envs=1)
        agent = CustomAgent(1, batched_env.num_actions, verbose=True)
        ascensions, scores = run_batched_rollout(1, batched_env, agent)

    print(
        f"Ascensions: {ascensions} "
        f"Median Score: {np.median(scores)}, "
        f"Mean Score: {np.mean(scores)}"
    )
    return np.median(scores)


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(
        description='Interactively replay a recorded playthrough.',
        add_help=True)

    parser.add_argument(
        '--seed', type=int, nargs=2, required=False, dest='seed',
        help='The seed pair to use. See `python -m nle_toolbox.utils.play replay.pkl`.',
    )

    parser.set_defaults(seed=None)

    args, _ = parser.parse_known_args()
    evaluate(**vars(args))
