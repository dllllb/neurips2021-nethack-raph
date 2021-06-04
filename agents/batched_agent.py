class BatchedAgent:
    """
    Simple Batched agent interface
    Main motivation is to speedup runs by increasing gpu utilization
    """
    def __init__(self, num_envs, num_actions):
        """
        Setup your model
        Load your weights etc
        """
        self.num_envs = num_envs
        self.num_actions = num_actions

    def preprocess_observations(self, observations, rewards, dones, infos):
        """
        Add any preprocessing steps, for example rerodering/stacking for torch/tf in your model
        """
        pass

    def preprocess_actions(self, actions):
        """
        Add any postprocessing steps, for example converting to lists
        """
        pass

    def batched_step(self):
        """
        Return a list of actions
        """
        pass
