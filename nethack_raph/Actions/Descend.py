import numpy as np

from nethack_raph.Actions.base import BaseAction
from nethack_raph.myconstants import COLOR_BG_GREEN


class Descend(BaseAction):
    def can(self, level):
        stairs = level.tiles.char == '>'
        self.log(f"Found {stairs.sum()} stairs")
        return stairs.any(), stairs

    def execute(self, path):
        *tail, one = path
        assert one == (self.hero.x, self.hero.y)
        if tail:
            self.log("Going towards stairs")
            self.draw_path(path, color=COLOR_BG_GREEN)
            self.hero.move(tail[-1])
            return

        if self.kernel().curTile().char != '>':
            self.log('door is absent')
            self.kernel().send(' ')

            # XXX raise False?
            return
        
        self.hero.descend()
