from nethack_raph.Actions.RandomWalk import *
from nethack_raph.Actions.Explore import *
from nethack_raph.Actions.AttackMonster import *
from nethack_raph.Actions.RangeAttackMonster import *
from nethack_raph.Actions.OpenDoors import *
from nethack_raph.Actions.Descend import *
from nethack_raph.Actions.Search import *
from nethack_raph.Actions.FixStatus import *
from nethack_raph.Actions.RestoreHP import *
from nethack_raph.Actions.Eat import *
from nethack_raph.Actions.Pray import Pray
from nethack_raph.Actions.PickUpStuff import PickUpStuff
from nethack_raph.Actions.Elbereth import Elbereth
from nethack_raph.Actions.UseItem import UseItem
from nethack_raph.Actions.ForceBolt import ForceBolt
from nethack_raph.Actions.Flash import Flash
from nethack_raph.Actions.EmergencyHeal import EmergencyHeal
from nethack_raph.Actions.FollowGuard import FollowGuard
from nethack_raph.Actions.Enhance import Enhance


class Brain:
    def __init__(self, name, kernel):
        self.kernel = kernel

        self.name = name
        self.kernel().personality.brains.append(self)

    def __str__(self):
        return "Brain(%s)" % self.name
