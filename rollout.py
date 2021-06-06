#!/usr/bin/env python

################################################################
## Ideally you shouldn't need to change this file at all      ##
##                                                            ##
## This file generates the rollouts, with the specific agent, ##
## batch_size and wrappers specified in subminssion_config.py ##
################################################################
from tqdm import tqdm
import numpy as np

from envs.batched_env import BactchedEnv
from submission_config import SubmissionConfig

NUM_ASSESSMENTS = 512

def run_batched_rollout(batched_env, agent):
    """
    This function will generate a series of rollouts in a batched manner.
    """

    num_envs = batched_env.num_envs

    # This part can be left as is
    observations = batched_env.batch_reset()
    rewards = [0.0 for _ in range(num_envs)]
    dones = [False for _ in range(num_envs)]
    infos = [{} for _ in range(num_envs)]

    # We assign each environment a fixed number of episodes at the start
    envs_each = NUM_ASSESSMENTS // num_envs
    remainders = NUM_ASSESSMENTS % num_envs
    episodes = [envs_each + int(i < remainders) for i in range(num_envs)]
    
    episode_count = 0
    pbar = tqdm(total=NUM_ASSESSMENTS)

    all_returns = []
    returns = [0.0 for _ in range(num_envs)]
    # The evaluator will automatically stop after the episodes based on the development/test phase
    while episode_count < NUM_ASSESSMENTS:
        actions = agent.batched_step(observations, rewards, dones, infos)

        observations, rewards, dones, infos = batched_env.batch_step(actions)
        
        for i, r in enumerate(rewards):
            returns[i] += r
        
        for done_idx in np.where(dones)[0]:
            observations[done_idx] = batched_env.single_env_reset(done_idx)
 
            if episodes[done_idx] > 0:
                all_returns.append(returns[done_idx])
                returns[done_idx] = 0.0
                episodes[done_idx] -= 1
                episode_count += 1
                pbar.update(1)
    return all_returns

if __name__ == "__main__":
    submission_env_make_fn = SubmissionConfig.submission_env_make_fn
    NUM_PARALLEL_ENVIRONMENTS = SubmissionConfig.NUM_PARALLEL_ENVIRONMENTS
    Agent = SubmissionConfig.Submision_Agent

    batched_env = BactchedEnv(
        env_make_fn=submission_env_make_fn, num_envs=NUM_PARALLEL_ENVIRONMENTS
    )

    num_envs = batched_env.num_envs
    num_actions = batched_env.num_actions

    agent = Agent(num_envs, num_actions)

    run_batched_rollout(batched_env, agent)
