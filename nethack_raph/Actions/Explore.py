from nethack_raph.Kernel import *
from nethack_raph.SignalReceiver import *
import numpy as np


class Explore(SignalReceiver):
    def __init__(self):
        SignalReceiver.__init__(self)

    def can(self):
        goal_coords = np.zeros((HEIGHT, WIDTH))

        if Kernel.instance.curLevel().explored:
            Kernel.instance.log("Level is explored.")
            return False, goal_coords

        Kernel.instance.log("No goals defined in Explore, finding one ..")
        found_unexplored = False
        for tile in Kernel.instance.curLevel().find(query={'explored': False, 'isWalkable': True, 'isHero': False}):
            goal_coords[tile.coords()] = True
            found_unexplored = True

        return found_unexplored, goal_coords

    def after_search(self, path):
        if path is None:
            Kernel.instance.log("Didn't find any goals.")
            Kernel.instance.curLevel().explored = True

    def execute(self, path):
        Kernel.instance.log("Found self.path (%s)" % str(path))
        path.draw(color=COLOR_BG_BLUE)
        Kernel.instance.Hero.move(path[1].tile)
