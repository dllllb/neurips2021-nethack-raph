import numpy as np

from agents.base import BatchedAgent
import nethack_raph.Kernel
from nethack_raph.myconstants import *
from nethack_raph.Personality import *
from nethack_raph.Senses import *
from nethack_raph.Console import *
from nethack_raph.Hero import *
from nethack_raph.Dungeon import *
from nethack_raph.MonsterSpoiler import *
from nethack_raph.Pathing import *
from nethack_raph.TestBrain import *
from nethack_raph.Cursor import *
from nethack_raph.ItemDB import *
from nethack_raph.Inventory import *

from nle.nethack.actions import ACTIONS


class CustomAgent(BatchedAgent):
    """A example agent... that simple acts randomly. Adapt to your needs!"""

    def __init__(self, num_envs, num_actions):
        """Set up and load you model here"""
        super().__init__(num_envs, num_actions)
        self.seeded_state = np.random.RandomState(42)
        Kernel(silent=False)

        # Stuff
        Console()
        Cursor()
        Dungeon()
        Hero()
        MonsterSpoiler()
        ItemDB()
        Inventory()

        # AI
        Personality()
        Senses()
        Pathing()

        # Brains
        curBrain = TestBrain()

        Kernel.instance.Personality.setBrain(curBrain)  # Default brain

        self.action2id = {
            chr(action.value): action_id for action_id, action in enumerate(ACTIONS)
        }

        self.action = ''

    def batched_step(self, observations, rewards, dones, infos):
        """
        Perform a batched step on lists of environment outputs.

        Each argument is a list of the respective gym output.
        Returns an iterable of actions.
        """

        assert len(dones) == 1
        # print(self.num_actions)

        while self.action == '':
            self.action = Kernel.instance.step(observations[0])

        ch = self.action[0]
        self.action = self.action[1:]
        Kernel.instance.log("Sent string:" + ch + ' ' + str(type(ch)))
        Kernel.instance.log("Sent string:" + ch + ' ' + str(self.action2id.get(ch)))
        return [self.action2id.get(ch)]
