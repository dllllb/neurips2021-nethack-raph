import gym

class EarlyTerminationNethack(gym.Wrapper):
    """
    To limit the timesteps for "Beginner" agents
    We terminate the episode early if  
        The minimum_score is not achieved without the cuttoff_timesteps

    Participants should not edit this file
    """
    def __init__(self, env, minimum_score=1000, cutoff_timesteps=50000):
        super().__init__(env)
        self._minimum_score = minimum_score
        self._cuttoff_timesteps = cutoff_timesteps
        self._elapsed_steps = None
        self._score = None

    def step(self, action):
        assert self._elapsed_steps is not None, "Cannot call env.step() before calling reset()"
        observation, reward, done, info = self.env.step(action)
        self._elapsed_steps += 1
        self._score += reward
        if self._elapsed_steps > self._cuttoff_timesteps and \
           self._score < self._minimum_score:
            info['Early Termination'] = not done
            done = True
        return observation, reward, done, info

    def reset(self, **kwargs):
        self._elapsed_steps = 0
        self._score = 0
        return self.env.reset(**kwargs)