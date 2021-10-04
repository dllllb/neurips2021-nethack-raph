from nethack_raph.myconstants import DUNGEON_HEIGHT, DUNGEON_WIDTH, COLOR_BG_BLUE

import numpy as np


class Explore:
    def __init__(self, kernel):
        self.kernel = kernel

    def can(self, level):
        if self.kernel().curLevel().explored:
            self.kernel().log("Level is explored.")
            return False, np.zeros((DUNGEON_HEIGHT, DUNGEON_WIDTH))

        targets = np.logical_not(level.tiles.explored) & level.tiles.walkable_tile & np.logical_not(level.tiles.is_hero)
        self.kernel().log(f"Found {targets.sum()} goals to explore")
        return targets.sum() > 0, targets

    def after_search(self, path):
        if path is None:
            self.kernel().log("Didn't find any goals.")
            self.kernel().curLevel().explored = True

    def execute(self, path):
        self.kernel().draw_path(path, color=COLOR_BG_BLUE)
        self.kernel().hero.move(path[-2])
