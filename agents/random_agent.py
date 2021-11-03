from agents.base import BatchedAgent
import numpy as np
from nethack_raph.rl_wrapper import RLActions


class RandomAgent(BatchedAgent):
    def __init__(self, num_envs, num_actions):
        super(RandomAgent, self).__init__(num_envs, num_actions)

    def batched_step(self, observations, rewards, dones, infos):
        actions = []
        for obs in observations:
            if not obs['rl_triggered']:
                actions.append(RLActions.CONTINUE)
                continue
            actions.append(np.random.choice(
                list(range(self.num_actions)), 1,
                p=obs['action_mask'] / np.sum(obs['action_mask'])
            ))

        return actions
