import numpy as np
from submission_config import SubmissionConfig, TestEvaluationConfig
from rollout import run_batched_rollout
from envs.batched_env import BatchedEnv
from envs.wrappers import create_env, TimeLimit
from nethack_raph.rl_wrapper import RLWrapper

from nle_toolbox.wrappers.replay import ReplayToFile


def env_make_fn(verbose=False):
    env = create_env()
    env = ReplayToFile(env, folder='test_merge', sticky=False)  # should be before RLWrapper
    env = TimeLimit(env, max_episode_steps=10_000_000)
    env = RLWrapper(env, verbose=verbose)
    return env


class RandomAgent:
    def __init__(self, n_envs, n_actions):
        self.n_envs = n_envs
        self.n_actions = n_actions
        self.log = open('msgs.txt', 'w')

    def batched_step(self, observations, rewards, dones, infos):
        actions = []
        for obs in observations:
            self.log.write(bytes(obs["message"][obs['message'].nonzero()]).decode('ascii') + '\n')
            actions.append(np.random.choice(
                list(range(self.n_actions)), 1,
                p=obs['action_mask'] / np.sum(obs['action_mask'])
            ))

        return actions


class OracleAgent:
    def __init__(self, n_envs, n_actions):
        self.n_envs = n_envs
        self.n_actions = n_actions
        self.offsets = [(-1, 0), (1, 0), (0, -1), (0, 1), (-1, -1), (-1, 1), (1, -1), (1, 1)]

    def batched_step(self, observations, rewards, dones, infos):
        result = np.zeros(len(observations), dtype=np.int32)
        for ibatch, obs in enumerate(observations):
            y, x = obs['blstats'][:2]
            tile_x, tile_y = obs['path'][-2]
            tile = (tile_x - x, tile_y - y)
            found = False
            for i, off in enumerate(self.offsets):
                if off == tile:
                    assert obs['action_mask'][i]
                    result[ibatch] = i
                    found = True
            assert found, f'tile = {tile}, hero = {x, y}, path = {obs["path"]}'
        return result


def evaluate():
    num_envs = 32
    Agent = SubmissionConfig.AGENT

    num_episodes = 128

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
