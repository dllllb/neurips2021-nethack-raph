#!/usr/bin/env python

############################################################
## Ideally you shouldn't need to change this file at all  ##
############################################################

import numpy as np

from envs.batched_env import BactchedEnv
from submission_config import SubmissionConfig

def run_batched_rollout(batched_env, agent):
    """
    This function will be called the rollout
    """

    num_envs = batched_env.num_envs

    # This part can be left as is
    observations = batched_env.batch_reset()
    rewards = [0.0 for _ in range(num_envs)]
    dones = [False for _ in range(num_envs)]
    infos = [{} for _ in range(num_envs)]

    episode_count = 0

    # The evaluator will automatically stop after the episodes based on the development/test phase
    while episode_count < 10000:
        actions = agent.batched_step(observations, rewards, dones, infos)

        observations, rewards, dones, infos = batched_env.batch_step(actions)
        for done_idx in np.where(dones)[0]:
            observations[done_idx] = batched_env.single_env_reset(done_idx)
            episode_count += 1
            print("Episodes Completed :", episode_count)

if __name__ == "__main__":

    submission_env_make_fn = SubmissionConfig.submission_env_make_fn
    NUM_PARALLEL_ENVIRONMENTS = SubmissionConfig.NUM_PARALLEL_ENVIRONMENTS
    Agent = SubmissionConfig.Submision_Agent

    batched_env = BactchedEnv(env_make_fn=submission_env_make_fn,
                              num_envs=NUM_PARALLEL_ENVIRONMENTS)

    num_envs = batched_env.num_envs
    num_actions = batched_env.num_actions

    agent = Agent(num_envs, num_actions)

    run_batched_rollout(batched_env, agent)

