## This file is intended to emulate the evaluation on AIcrowd

# IMPORTANT - Differences to expect
# * All the environment's functions are not available
# * The run might be slower than your local run
# * Resources might vary from your local machine

import numpy as np

from submission_config import SubmissionConfig, TestEvaluationConfig

from rollout import run_batched_rollout
from envs.batched_env import BatchedEnv


def evaluate():
    env_make_fn = SubmissionConfig.MAKE_ENV_FN
    num_envs = SubmissionConfig.NUM_ENVIRONMENTS
    Agent = SubmissionConfig.AGENT

    num_episodes = TestEvaluationConfig.NUM_EPISODES

    batched_env = BatchedEnv(env_make_fn=env_make_fn, num_envs=num_envs)

    agent = Agent(num_envs, batched_env.num_actions)

    ascensions, scores = run_batched_rollout(num_episodes, batched_env, agent)
    print(
        f"Ascensions: {ascensions} "
        f"Median Score: {np.median(scores)}, "
        f"Mean Score: {np.mean(scores)}"
    )


if __name__ == "__main__":
    evaluate()
