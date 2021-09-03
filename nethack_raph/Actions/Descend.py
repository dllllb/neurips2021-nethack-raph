from nethack_raph.Kernel import *
import numpy as np


class Descend:
    def __init__(self):
        pass

    def can(self):
        goal_coords = np.zeros((HEIGHT, WIDTH))

        Kernel.instance.log("Finding '>' ..")
        stairs = Kernel.instance.curLevel().find({'glyph': '>'})
        Kernel.instance.log(f"Found {len(stairs)} stairs")
        for stair in stairs: # Grammar <3
            goal_coords[stair.coords()] = True
        return len(stairs), goal_coords

    def after_search(self, path):
        pass

    def execute(self, path):
        if len(path) == 1:
            if path[0].tile.glyph == '>':
                Kernel.instance.Hero.descend()
                return
            Kernel.instance.log('door is absent')
            Kernel.instance.send(' ')
            return

        Kernel.instance.log("Going towards stairs")
        path.draw(color=COLOR_BG_GREEN)
        Kernel.instance.Hero.move(path[1].tile)
