## This file is intended to emulate the evaluation on AIcrowd

# IMPORTANT - Differences to expect
# * All the environment's functions are not available
# * The run might be slower than your local run
# * Resources might vary from your local machine

from submission_agent import SubmissionConfig, LocalEvaluationConfig
                              
from rollout import run_batched_rollout
from nethack_baselines.utils.batched_env import BactchedEnv


# Ideally you shouldn't need to change anything below
def add_evaluation_wrappers_fn(env_make_fn):
    max_episodes = LocalEvaluationConfig.LOCAL_EVALUATION_NUM_EPISODES
    # TOOD: use LOCAL_EVALUATION_NUM_EPISODES for limiting episodes
    return env_make_fn

def evaluate():
    submission_env_make_fn = SubmissionConfig.submission_env_make_fn
    num_envs = SubmissionConfig.NUM_PARALLEL_ENVIRONMENTS 
    Agent = SubmissionConfig.Submision_Agent

    evaluation_env_fn = add_evaluation_wrappers_fn(submission_env_make_fn)
    batched_env = BactchedEnv(env_make_fn=evaluation_env_fn,
                                num_envs=num_envs)

    num_envs = batched_env.num_envs
    num_actions = batched_env.num_actions

    agent = Agent(num_envs, num_actions)

    run_batched_rollout(batched_env, agent)
    

if __name__ == '__main__':
    evaluate()
