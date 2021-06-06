import numpy as np

from agents.batched_agent import BatchedAgent

class RandomAgent(BatchedAgent):
    """This random agent just selects an action from the action space."""
    def __init__(self, num_envs, num_actions):
        super().__init__(num_envs, num_actions)
        self.seeded_state = np.random.RandomState(42)

    def batched_step(self, observations, rewards, dones, infos):
        actions = self.seeded_state.randint(self.num_actions, size=self.num_envs)
        return actions