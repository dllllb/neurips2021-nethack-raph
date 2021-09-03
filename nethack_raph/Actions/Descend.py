from nethack_raph.Kernel import *


class Descend:
    def __init__(self):
        self.path = None
        self.on_stairs = False

    def can(self):
        self.path = None
        self.on_stairs = False

        if Kernel.instance.curTile().glyph == '>':
            Kernel.instance.log("We're standing on '>'. Let's descend!")
            self.on_stairs = True
            return True

        Kernel.instance.log("Finding '>' ..")
        stairs = Kernel.instance.curLevel().find({'glyph': '>'})
        for stair in stairs: # Grammar <3
            Kernel.instance.log("Found one (%s)" % str(stair))
            path = Kernel.instance.Pathing.a_star_search(end=stair)
            if path and (self.path is None or self.path.g > path.g):
                self.path = path

        if self.path:
            Kernel.instance.log("Path: %s" % self.path)
            return True
        return False

    def execute(self):
        if self.on_stairs:
            Kernel.instance.Hero.descend()
        else:
            Kernel.instance.log("Going towards stairs")
            self.path.draw(color=COLOR_BG_GREEN)
            Kernel.instance.Hero.move(self.path[1].tile)
