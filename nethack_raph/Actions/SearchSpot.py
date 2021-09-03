from nethack_raph.Kernel import *
import numpy as np


class SearchSpot:
    def __init__(self):
        self.goal = None

    def can(self):
        goal_coords = np.zeros((HEIGHT, WIDTH))
        self.goal = None

        unsearched = Kernel.instance.curTile().adjacent({'walkable': False, 'searched': False})
        if len(unsearched) > 4 and len(Kernel.instance.curTile().straight({'walkable': True})) == 1:
            for tile in Kernel.instance.curTile().neighbours():
                if tile.is_door: # So it won't search on "###@]  "
                    return False, np.zeros((HEIGHT, WIDTH))
            self.goal = sorted(unsearched, key=lambda x: x.searches)[0]

            #FIXME (dima) add all?
            goal_coords[self.goal.coords()] = True
            return True, goal_coords

        return False, goal_coords

    def after_search(self, path):
        pass

    def execute(self, path):
        Kernel.instance.log("Searching..")
        Kernel.instance.drawString("Searching hotspot (%s)" % self.goal)
        Kernel.instance.Hero.search()
        if self.goal.searches >= 10:
            self.goal.searched = True
            self.goal = None
