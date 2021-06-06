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

    def batched_step(self, observations, rewards, dones, infos):
        """
        Take list of outputs of each environments and return a list of actions
        """
        raise NotImplementedError

