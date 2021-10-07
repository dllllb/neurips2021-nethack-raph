import numpy as np

from nethack_raph.Actions.base import BaseAction
from nethack_raph.myconstants import COLOR_BG_YELLOW


class Search(BaseAction):
    mask = np.array([
        [1, 1, 1],
        [1, 0, 1],
        [1, 1, 1],
    ], dtype=bool)

    def can(self, level):
        self.log("Finding possible searchwalktos")

        adj, tiles = level.neighbours, level.tiles
        # unexplored, walkable tiles, neighbours of unsearched tiles (not exactly as it was before)
        targets = np.isin(adj.char, ('|', '-', ' ')) & self.mask
        targets &= ~adj.searched & ~adj.in_shop

        targets = targets.sum((-1, -2))
        targets *= tiles.walkable_tile & tiles.explored
        if targets.max() == 0:
            return False, None
        else:
            targets = targets == targets.max()
            return True, targets

    def after_search(self, path):
        if path is None:
            level = self.kernel().curLevel()
            self.log(f"Didn't find a path to searchspot. Clear searched")
            level.maxSearches = level.maxSearches + 60
            level.tiles.searched = False

    def execute(self, path):
        *tail, one = path
        hero = self.hero
        assert one == (hero.x, hero.y)

        if tail:
            self.log("Going towards searchspot")
            self.draw_path(path, color=COLOR_BG_YELLOW)
            self.hero.move(tail[-1])
            return

        self.hero.search(60)
