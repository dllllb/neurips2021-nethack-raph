from nethack_raph.myconstants import DUNGEON_HEIGHT, DUNGEON_WIDTH, COLOR_BG_YELLOW

import numpy as np


class Search:
    def __init__(self, kernel):
        self.kernel = kernel
        self.mask = np.array([[1, 1, 1], [1, 0, 1], [1, 1, 1]])

    def can(self, level):
        self.kernel().log("Finding possible searchwalktos")

        # unexplored, walkable tiles, neighbours of unsearched tiles (not exactly as it was before)
        targets = np.isin(level.neighbours.char, ('|', '-', ' ')) & np.logical_not(level.neighbours.searched)
        targets = targets & np.logical_not(level.neighbours.in_shop)
        targets = (targets * self.mask).sum((-1, -2))
        targets *= (level.tiles.walkable_tile & level.tiles.explored)

        if targets.max() == 0:
            return False, targets
        else:
            targets = targets == targets.max()
            return True, targets

    def after_search(self, path):
        if path is None:
            self.kernel().log(f"Didn't find a path to searchspot. Clear searched")
            self.kernel().curLevel().maxSearches = self.kernel().curLevel().maxSearches + 5
            self.kernel().curLevel().tiles.searched = False

    def execute(self, path):
        if len(path) == 1:
            assert path[0] == tuple(self.kernel().curTile().xy)
            self.kernel().hero.search(2)
            return

        self.kernel().log("Going towards searchspot")
        self.kernel().draw_path(path, color=COLOR_BG_YELLOW)
        self.kernel().hero.move(path[-2])
