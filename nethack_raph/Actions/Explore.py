from nethack_raph.myconstants import HEIGHT, WIDTH, COLOR_BG_BLUE

import numpy as np


class Explore:
    def __init__(self, kernel):
        self.kernel = kernel

    def can(self):
        goal_coords = np.zeros((HEIGHT, WIDTH))

        if self.kernel().curLevel().explored:
            self.kernel().log("Level is explored.")
            return False, goal_coords

        self.kernel().log("No goals defined in Explore, finding one ..")
        found_unexplored = False
        for tile in filter(lambda t: not t.explored and t.isWalkable() and not t.isHero(), self.kernel().curLevel().tiles):
            goal_coords[tile.coords()] = True
            found_unexplored = True

        return found_unexplored, goal_coords

    def after_search(self, path):
        if path is None:
            self.kernel().log("Didn't find any goals.")
            self.kernel().curLevel().explored = True

    def execute(self, path):
        self.kernel().log("Found self.path (%s)" % str(path))
        self.kernel().draw_path(path, color=COLOR_BG_BLUE)
        self.kernel().hero.move(path[-2])
