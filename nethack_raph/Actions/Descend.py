from nethack_raph.myconstants import HEIGHT, WIDTH, COLOR_BG_GREEN

import numpy as np


class Descend:
    def __init__(self, kernel):
        self.kernel = kernel

    def can(self):
        goal_coords = np.zeros((HEIGHT, WIDTH))

        self.kernel().log("Finding '>' ..")
        stairs = list(filter(lambda tile: tile.glyph == '>', self.kernel().curLevel().tiles))
        self.kernel().log(f"Found {len(stairs)} stairs")
        for stair in stairs: # Grammar <3
            goal_coords[stair.coords()] = True
        return len(stairs), goal_coords

    def after_search(self, path):
        pass

    def execute(self, path):
        if len(path) == 1:
            if path[0].glyph == '>':
                self.kernel().hero.descend()
                return
            self.kernel().log('door is absent')
            self.kernel().send(' ')
            return

        self.kernel().log("Going towards stairs")
        self.kernel().draw_path(path, color=COLOR_BG_GREEN)
        self.kernel().hero.move(path[-2])
