from nethack_raph.myconstants import DUNGEON_HEIGHT, DUNGEON_WIDTH, COLOR_BG_GREEN

import numpy as np


class Descend:
    def __init__(self, kernel):
        self.kernel = kernel

    def can(self, level):
        self.kernel().log("Finding '>' ..")
        stairs = level.tiles.char == '>'
        self.kernel().log(f"Found {stairs.sum()} stairs")
        return stairs.sum() > 0, stairs

    def after_search(self, path):
        pass

    def execute(self, path):
        if len(path) == 1:
            assert path[0] == tuple(self.kernel().curTile().xy)
            if self.kernel().curTile().char == '>':
                self.kernel().hero.descend()
                return
            self.kernel().log('door is absent')
            self.kernel().send(' ')
            return

        self.kernel().log("Going towards stairs")
        self.kernel().draw_path(path, color=COLOR_BG_GREEN)
        self.kernel().hero.move(path[-2])
