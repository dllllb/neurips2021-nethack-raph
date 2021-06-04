import numpy as np

from agents.batched_agent import BatchedAgent

class RandomAgent(BatchedAgent):
    def __init__(self, num_envs, num_actions):
        super().__init__(num_envs, num_actions)
        self.seeded_state = np.random.RandomState(42)

    def preprocess_observations(self, observations, rewards, dones, infos):
        return observations, rewards, dones, infos

    def postprocess_actions(self, actions):
        return actions

    def batched_step(self, observations, rewards, dones, infos):
        rets = self.preprocess_observations(observations, rewards, dones, infos)
        observations, rewards, dones, infos = rets
        actions = self.seeded_state.randint(self.num_actions, size=self.num_envs)
        actions = self.postprocess_actions(actions)
        return actions