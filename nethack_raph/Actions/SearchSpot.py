from nethack_raph.myconstants import HEIGHT, WIDTH

import numpy as np


class SearchSpot:
    def __init__(self, kernel):
        self.goal = None
        self.kernel = kernel

    def can(self):
        goal_coords = np.zeros((HEIGHT, WIDTH))
        self.goal = None

        unsearched = self.kernel().curTile().adjacent({'walkable': False, 'searched': False})
        if len(unsearched) > 4 and len(self.kernel().curTile().straight({'walkable': True})) == 1:
            for tile in self.kernel().curTile().neighbours():
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
        self.kernel().log("Searching..")
        self.kernel().drawString("Searching hotspot (%s)" % self.goal)
        self.kernel().hero.search()
        if self.goal.searches >= 10:
            self.goal.searched = True
            self.goal = None
