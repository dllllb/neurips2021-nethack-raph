import numpy as np

from agents.base import BatchedAgent
from nethack_dqn.dqn_model import DQNAgent, DuelDQNModel
import torch


class CustomAgent(BatchedAgent):
    """A example agent... that simple acts randomly. Adapt to your needs!"""

    def __init__(self, num_envs, num_actions):
        """Set up and load you model here"""
        super().__init__(num_envs, num_actions)
        self.seeded_state = np.random.RandomState(42)

        self.device = torch.device('cuda:0')
        model = DuelDQNModel(input_shape=(21, 79), n_actions=4)
        model.load_state_dict(torch.load('/Users/sodi/dev/sber/neurips-2021-the-nethack-challenge/saved_models/dqn/model'))
        self.impl = DQNAgent(model, epsilon=0.01, device=self.device)

    def batched_step(self, observations, rewards, dones, infos):
        """
        Perform a batched step on lists of environment outputs.

        Each argument is a list of the respective gym output.
        Returns an iterable of actions.
        """
        # print(self.num_actions)
        observations = self.batch_inputs(observations)

        # print(observations[0])
        actions = self.impl.sample_actions(observations['chars'])
        return actions

    def batch_inputs(self, observations):
        states = list(observations[0].keys())
        obs = {k: [] for k in states}

        # Unpack List[Dicts] -> Dict[Lists]
        for o in observations:
            for k, t in o.items():
                obs[k].append(t)

        # Convert to Tensor, Add Unroll Dim (=1), Move to GPU
        for k in states:
            obs[k] = torch.Tensor(np.stack(obs[k])).to(self.device)
        return obs
