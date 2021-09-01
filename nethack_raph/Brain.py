from nethack_raph.SignalReceiver import *

from nethack_raph.Actions.RandomWalk import *
from nethack_raph.Actions.Explore import *
from nethack_raph.Actions.AttackMonster import *
from nethack_raph.Actions.OpenDoors import *
from nethack_raph.Actions.GetPhatz import *
from nethack_raph.Actions.Descend import *
from nethack_raph.Actions.Search import *
from nethack_raph.Actions.SearchSpot import *
from nethack_raph.Actions.FixStatus import *
from nethack_raph.Actions.RestoreHP import *
from nethack_raph.Actions.DipForExcalibur import *
from nethack_raph.Actions.Eat import *


class Brain(SignalReceiver):
    def __init__(self, name):
        SignalReceiver.__init__(self)

        self.name = name
        Kernel.instance.Personality.brains.append(self)

    def __str__(self):
        return "Brain(%s)" % self.name
