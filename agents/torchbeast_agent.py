import torch
import numpy as np

from agents.base import BatchedAgent

from nethack_baselines.torchbeast.models import load_model

MODEL_DIR = "./saved_models/torchbeast/pretrained_0.5B"


class TorchBeastAgent(BatchedAgent):
    """
    A BatchedAgent using the TorchBeast Model
    """

    def __init__(self, num_envs, num_actions):
        super().__init__(num_envs, num_actions)
        self.model_dir = MODEL_DIR
        self.device = "cuda:0" if torch.cuda.is_available() else "cpu"
        self.model = load_model(MODEL_DIR, self.device)
        print(f'Using Model In: {self.model_dir}, Device: {self.device}')

        self.core_state = [
            m.to(self.device) for m in self.model.initial_state(batch_size=num_envs)
        ]

    def batch_inputs(self, observations, dones):
        """
        Convert lists of observations, rewards, dones, infos to tensors for TorchBeast.

        TorchBeast models:
            * take tensors in the form: [T, B, ...]: B:= batch, T:= unroll (=1)
            * take "done" as a BOOLEAN observation
        """
        states = list(observations[0].keys())
        obs = {k: [] for k in states}

        # Unpack List[Dicts] -> Dict[Lists]
        for o in observations:
            for k, t in o.items():
                obs[k].append(t)

        # Convert to Tensor, Add Unroll Dim (=1), Move to GPU
        for k in states:
            obs[k] = torch.Tensor(np.stack(obs[k])[None, ...]).to(self.device)
        obs["done"] = torch.Tensor(np.array(dones)[None, ...]).bool().to(self.device)
        return obs, dones

    def batched_step(self, observations, rewards, dones, infos):
        """
        Perform a batched step on lists of environment outputs.

        Torchbeast models:
            * take the core (LSTM) state as input, and return as output
            * return outputs as a dict of "action", "policy_logits", "baseline"
        """
        observations, dones = self.batch_inputs(observations, dones)

        with torch.no_grad():
            outputs, self.core_state = self.model(observations, self.core_state)

        return outputs["action"].cpu().numpy()[0]
