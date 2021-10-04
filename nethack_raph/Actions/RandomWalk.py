from nethack_raph.myconstants import DUNGEON_HEIGHT, DUNGEON_WIDTH

import numpy as np


class RandomWalk:
    def __init__(self, kernel):
        self.kernel = kernel

    def can(self, level):
        targets = \
            np.logical_not(level.tiles.visited) & level.tiles.walkable_tile & \
            np.logical_not(level.tiles.is_hero) & (level.tiles.char == '.') & \
            np.logical_not(level.tiles.in_shop)
        return targets.sum() > 0, targets

    def after_search(self, path):
        if path is None:
            self.kernel().curLevel().tiles.visited = False
        self.kernel().hero.search(30)

    def execute(self, path):
        self.kernel().hero.move(path[-2])
        queue = [self.kernel().curTile()]
        while queue:
            front = queue.pop()
            if front.char == '.' and not front.visited:
                self.kernel().curLevel().tiles[front.xy.x, front.xy.y].visited = True
                queue.extend(self.kernel().curLevel().get_neighbours(front))
