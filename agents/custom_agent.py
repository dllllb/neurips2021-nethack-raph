from agents.base import BatchedAgent
from nethack_raph.Kernel import Kernel


from nle.nethack.actions import ACTIONS
import time


class CustomAgent(BatchedAgent):
    """A example agent... that simple acts randomly. Adapt to your needs!"""
    def __init__(self, num_envs, num_actions):
        """Set up and load you model here"""
        super().__init__(num_envs, num_actions)
        self.kernel = Kernel(silent=True)

        self.action2id = {
            chr(action.value): action_id for action_id, action in enumerate(ACTIONS)
        }

        self.maxtime = 0

    def batched_step(self, observations, rewards, dones, infos):
        """
        Perform a batched step on lists of environment outputs.

        Each argument is a list of the respective gym output.
        Returns an iterable of actions.
        """

        assert len(dones) == 1

        if int(dones[0]):
            del self.kernel
            self.kernel = Kernel(silent=False)

        before = time.time()

        action = self.kernel.step(observations[0])
        if len(action):
            ch = action[0]
        else:
            #TODO check if it happens
            ch = ' '

        action = self.action2id.get(ch)
        if action is None:
            #TODO check if it happens
            action = 0

        after = time.time()
        self.maxtime = max(self.maxtime, after - before)

        self.kernel.log("Sent string:" + ch + ' ' + str(type(ch)))
        self.kernel.log("Sent string:" + ch + ' ' + str(action))
        self.kernel.log(f'action time: {after - before}, maxtime: {self.maxtime}')
        return [action]
