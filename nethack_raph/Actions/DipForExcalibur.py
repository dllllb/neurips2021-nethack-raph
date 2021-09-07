from nethack_raph.Kernel import *

class DipForExcalibur:
    def __init__(self):
        self.path = None
        self.dip = False

    def can(self):
        if self.kernel().curTile().glyph == '}':
            excal = self.kernel().Inventory.search({'appearance': 'long sword'}, getFirst=True)
            if excal:
                self.item = excal
                self.path = None
                self.dip = True
                return True

        if self.path and self.path.isWalkable():
            return True

        if self.kernel().hero.xp >= 5 and not self.kernel().ItemDB.find({'appearance': 'Excalibur'}):
            for tile in self.kernel().curLevel().find({'glyph': '{'}):
                path = self.kernel().pathing.path(end=tile)
                if path:
                    self.path = path
        else:
            self.path = None
            return False

        return self.path and True or False

    def execute(self):
        if self.dip:
            self.kernel().log("Dipping for excalibur.")
            self.kernel().hero.dip( self.item )
        else:
            self.path.draw(color=COLOR_GREEN)
            self.kernel().log("Walking towards a fountain.")
            self.kernel().hero.move(self.path[-2].tile)
