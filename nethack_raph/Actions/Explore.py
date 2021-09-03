from nethack_raph.Kernel import *
from nethack_raph.SignalReceiver import *
import time


class Explore(SignalReceiver):
    def __init__(self):
        SignalReceiver.__init__(self)
        self.path = None

    def can(self):
        if Kernel.instance.curLevel().explored:
            Kernel.instance.log("Level is explored.")
            return False

        Kernel.instance.log("No goals defined in Explore, finding one ..")
        self.path = Kernel.instance.Pathing.a_star_search(find={'explored': False, 'isWalkable': True, 'isHero': False})
        if not self.path:
            Kernel.instance.log("Didn't find any goals.")
            Kernel.instance.curLevel().explored = True
            return False

        Kernel.instance.log("Found one (%s)" % str(self.path[-1].tile))
        return True

    def execute(self):
        Kernel.instance.log("Found self.path (%s)" % str(self.path))
        self.path.draw(color=COLOR_BG_BLUE)
        Kernel.instance.Hero.move(self.path[1].tile)

    def new_dlvl(self):
        self.interrupt_action()

    def interrupt_action(self, action=None):
        if action != self:
            self.path = None
            self.goal = None
            Kernel.instance.log("Explorer got interrupted by %s" % str(action))
