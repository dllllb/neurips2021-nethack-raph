import numpy as np

from agents.base import BatchedAgent


class CustomAgent(BatchedAgent):
    """A example agent... that simple acts randomly. Adapt to your needs!"""

    def __init__(self, num_envs, num_actions):
        """Set up and load you model here"""
        super().__init__(num_envs, num_actions)
        self.seeded_state = np.random.RandomState(42)

    def batched_step(self, observations, rewards, dones, infos):
        """
        Perform a batched step on lists of environment outputs.

        Each argument is a list of the respective gym output.
        Returns an iterable of actions.
        """
        actions = self.seeded_state.randint(self.num_actions, size=self.num_envs)
        return actions
