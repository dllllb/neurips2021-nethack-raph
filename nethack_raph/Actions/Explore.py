from nethack_raph.Kernel import *
from nethack_raph.SignalReceiver import *
import time


class Explore(SignalReceiver):
    def __init__(self):
        SignalReceiver.__init__(self)

        self.goal = None
        self.path = None
        self.recursion_depth = 0

    def can(self):
        # FIXME (dima) check logick
        if self.recursion_depth > 15:
            self.recursion_depth = 0
            return False

        self.recursion_depth += 1

        if Kernel.instance.curLevel().explored:
            Kernel.instance.log("Level is explored.")
            self.recursion_depth = 0
            return False

        if self.goal and self.goal == Kernel.instance.curTile():
            Kernel.instance.log("Goal has been reached in Explore")
            self.goal = None

        if self.goal and not self.goal.isWalkable():
            Kernel.instance.log("Goal has be switched to unwalkable.")
            self.goal = None

        if not self.goal:
            Kernel.instance.log("No goals defined in Explore, finding one ..")
            goalNode = Kernel.instance.Pathing.path(find={'explored': False, 'isWalkable': True, 'isHero': False})
            if not goalNode:
                Kernel.instance.log("Didn't find any goals.")
                Kernel.instance.curLevel().explored = True
                self.recursion_depth = 0
                return False
            else:
                Kernel.instance.log("Found one (%s)" % str(goalNode))
                self.goal = goalNode.tile

        if self.path and self.path.isWalkable():
            a = self.path
            while a.parent != 0:
                a = a.parent
            if Kernel.instance.curTile() == a.tile:
                self.recursion_depth = 0
                return True

        self.path = Kernel.instance.Pathing.path(end=self.goal)
        if not self.path:
            self.goal = None
            self.path = None
            return self.can()
        self.recursion_depth = 0
        return True

    def execute(self):
        Kernel.instance.log("Found self.path (%s)" % str(self.path))
        self.path.draw(color=COLOR_BG_BLUE)
        Kernel.instance.Hero.move(self.path[-2].tile)

    def new_dlvl(self):
        self.interrupt_action()

    def interrupt_action(self, action=None):
        if action != self:
            self.path = None
            self.goal = None
            Kernel.instance.log("Explorer got interrupted by %s" % str(action))
