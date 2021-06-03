import aicrowd_gym
import nle
import numpy as np
from tqdm import trange
from custom_wrappers import EarlyTerminationNethack

from batched_env import BactchedEnv

class BatchedAgent:
    """
    Simple Batched agent interface
    Main motivation is to speedup runs by increasing gpu utilization
    """
    def __init__(self, num_envs):
        """
        Setup your model
        Load your weights etc
        """
        self.num_envs = num_envs

    def preprocess_observations(self, observations, rewards, dones, infos):
        """
        Add any preprocessing steps, for example rerodering/stacking for torch/tf in your model
        """
        pass

    def batched_step(self):
        """
        Return a list of actions
        """
        pass

class RandomBatchedAgent(BatchedAgent):
    def __init__(self, num_envs, num_actions):
        super().__init__(num_envs)
        self.num_actions = num_actions
        self.seeded_state = np.random.RandomState(42)

    def preprocess_observations(self, observations, rewards, dones, infos):
        return observations, rewards, dones, infos

    def batched_step(self, observations, rewards, dones, infos):
        rets = self.preprocess_observations(observations, rewards, dones, infos)
        observations, rewards, dones, infos = rets
        actions = self.seeded_state.randint(self.num_actions, size=self.num_envs)
        return actions


if __name__ == '__main__':

    def nethack_make_fn():
        
        # These settings will be fixed by the aicrowd evaluator
        env = aicrowd_gym.make('NetHackChallenge-v0',
                         observation_keys=("glyphs",
                                          "chars",
                                          "colors",
                                          "specials",
                                          "blstats",
                                          "message",
                                          "tty_chars",
                                          "tty_colors",
                                          "tty_cursor",))

        # This wrapper will always be added on the aicrowd evaluator
        env = EarlyTerminationNethack(env=env,
                    minimum_score=1000,
                    cutoff_timesteps=50000)
        
        # Add any wrappers you need

        return env


    # Change the num_envs as you need, for example reduce if your GPU doesn't fit
    # but increasing above 32 is not advisable for the Nethack Challenge 2021
    num_envs = 16
    batched_env = BactchedEnv(env_make_fn=nethack_make_fn, num_envs=num_envs)

    # This part can be left as is
    observations = batched_env.batch_reset()
    rewards = [0.0 for _ in range(num_envs)]
    dones = [False for _ in range(num_envs)]
    infos = [{} for _ in range(num_envs)]

    # Change this to your agent interface
    num_actions = batched_env.envs[0].action_space.n
    agent = RandomBatchedAgent(num_envs, num_actions)
    
    # The evaluation setup will automatically stop after the requisite number of rollouts
    # But you can change this if you want
    for _ in trange(1000000000000): 

        # Ideally this part can be left unchanged
        actions = agent.batched_step(observations, rewards, dones, infos) 

        observations, rewards, dones, infos = batched_env.batch_step(actions)
        for done_idx in np.where(dones)[0]:
            observations[done_idx] = batched_env.single_env_reset(done_idx) 
