import numpy as np
from submission_config import SubmissionConfig, TestEvaluationConfig
from rollout import run_batched_rollout
from envs.batched_env import BatchedEnv

from nle_toolbox.wrappers.replay import ReplayToFile


def env_make_fn():
    env = SubmissionConfig.MAKE_ENV_FN()
    return ReplayToFile(env, folder='ttys', sticky=False)


def evaluate():
    num_envs = 32
    Agent = SubmissionConfig.AGENT

    num_episodes = 32

    batched_env = BatchedEnv(env_make_fn=env_make_fn, num_envs=num_envs)

    agent = Agent(num_envs, batched_env.num_actions)

    ascensions, scores = run_batched_rollout(num_episodes, batched_env, agent)
    print(
        f"Ascensions: {ascensions} "
        f"Median Score: {np.median(scores)}, "
        f"Mean Score: {np.mean(scores)}"
    )
    return np.median(scores)


if __name__ == "__main__":
    evaluate()
