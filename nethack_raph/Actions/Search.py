from nethack_raph.myconstants import DUNGEON_HEIGHT, DUNGEON_WIDTH, COLOR_BG_YELLOW

import numpy as np


class Search:
    def __init__(self, kernel):
        self.kernel = kernel

    def can(self):
        target_tiles = np.zeros((DUNGEON_HEIGHT, DUNGEON_WIDTH))
        found = False

        self.kernel().log("Finding possible searchwalktos")

        for tile in filter(lambda t: not t.walkable_tile and not t.searched and t.char in {'|', '-', ' '}, self.kernel().curLevel().tiles):
            # TODO should preoritize them by count = len([x for x in neighbour.adjacent({'searched': False})])
            neighbours = list(filter(lambda t: t.explored and t.walkable_glyph and (t.monster is None or not t.monster.pet), tile.neighbours()))
            if len(neighbours):
                walkto = max(neighbours, key=lambda t: len([neigh for neigh in t.neighbours() if not neigh.searched]))
                target_tiles[walkto.coords()] = True
                found = True
        return found, target_tiles

    def after_search(self, path):
        if path is None:
            self.kernel().curLevel().maxSearches = self.kernel().curLevel().maxSearches + 5
            for tile in self.kernel().curLevel().tiles:
                tile.searched = False

    def execute(self, path):
        if len(path) == 1:
            assert path[0] == self.kernel().curTile()
            self.kernel().hero.search(2)
            return

        self.kernel().log("Going towards searchspot")
        self.kernel().draw_path(path, color=COLOR_BG_YELLOW)
        self.kernel().hero.move(path[-2])
        # self.kernel().sendSignal('interrupt_action', self)
