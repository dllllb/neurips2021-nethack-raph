from nethack_raph.myconstants import DUNGEON_HEIGHT, DUNGEON_WIDTH, COLOR_BG_CYAN

import numpy as np


class OpenDoors:
    def __init__(self, kernel):
        self.kernel = kernel
        self.mask = np.array([[0, 1, 0], [1, 0, 1], [0, 1, 0]])

    def can(self, level):
        # all unexplored, walkable neighbours of closed door
        doors = (level.neighbours.is_closed_door & np.logical_not(level.neighbours.shopkeep_door))
        doors = (doors * self.mask).sum((-1, -2)) > 0
        doors &= (level.tiles.walkable_tile & level.tiles.explored)

        self.kernel().log(f"found door: {doors.sum() > 0}, {doors.nonzero()}")
        return doors.sum() > 0, doors

    def after_search(self, path):
        pass

    def execute(self, path):
        if len(path) == 1:
            assert path[0] == tuple(self.kernel().curTile().xy)
            neighbours = self.kernel().curLevel().neighbours[self.kernel().hero.coords()]
            for tile in neighbours[neighbours.is_closed_door]:
                if tile.locked:
                    self.kernel().hero.kick(tuple(tile.xy))
                else:
                    self.kernel().hero.open(tuple(tile.xy))
                return

            self.kernel().log('door is absent')
            self.kernel().send(' ')
            return
        else:
            self.kernel().draw_path(path, color=COLOR_BG_CYAN)
            self.kernel().hero.move(path[-2])
