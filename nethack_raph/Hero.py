from nethack_raph.TermColor import TermColor


class Hero:
    def __init__(self, kernel):
        self.kernel = kernel
        self.x = None
        self.y = None
        self.beforeMove = None
        self.tmpCount = 0

        self.blind = False
        self.legShape = True

        self.inBearTrap = False
        self.inPit = False
        self.isEngulfed = False
        self.isPolymorphed = False

        self.hanger = None
        self.have_food = True
        self.god_is_angry = False

        self.lastActionedTile = None # I sersiouly need to #enhance my english skills :'(

    def coords(self):
        return self.y, self.x

    def attack(self, tile):
        dir = self._get_direction(self.kernel().curTile(), tile)
        self.kernel().drawString("Attacking -> %s (%s)" % (dir, tile))
        self.kernel().send("F"+dir)
        self.lastActionedTile = tile

    def move(self, tile):
        if self.beforeMove == (self.x,self.y) and self.tmpCount < 5 and not (self.inBearTrap or self.inPit):
            self.kernel().log("Hero asked to move, but I still havn't moved after last update, ignoring this")
            self.tmpCount = self.tmpCount + 1
        else:
            if self.beforeMove != (self.x, self.y):
                self.inBearTrap = False
                self.inPit = False
            else:
                if self.tmpCount > 3:
                    if not tile.glyph:
                        self.kernel().log("Made a door at %s" % tile)
                        tile.glyph = '-'
                        tile.color = TermColor(33, 0, False, False)
                        self.kernel().sendSignal("interrupt_action")

            dir = self._get_direction(self.kernel().curTile(), tile)
            self.kernel().drawString("Walking -> %s (%s)" % (dir, tile))

            self.beforeMove = (self.x,self.y)
            self.tmpCount = 0

            self.lastActionedTile = tile
            self.kernel().send(dir)

    def descend(self):
        self.kernel().log("Hero is descending..")
        self.kernel().send(">")
        self.kernel().dontUpdate()

    def open(self, tile):
        dir = self._get_direction(self.kernel().curTile(), tile)
        self.kernel().log("Hero is opening a door..")
        self.kernel().send("o%s" % dir)
        self.lastActionedTile = tile

    def kick(self, tile):
        dir = self._get_direction(self.kernel().curTile(), tile)
        self.kernel().log("Hero is kicking a door..")
        self.kernel().send("\x04%s" % dir)

    def search(self, times=2):
        self.kernel().send("%ds" % times)
        for neighbour in self.kernel().curTile().neighbours():
            neighbour.searches = neighbour.searches + 1
            if neighbour.searches == self.kernel().curLevel().maxSearches:
                neighbour.searched = True

    def eat(self):
        self.kernel().log("Hero::eat")
        self.kernel().send("e")

    def can_eat(self, tile):
        return len([item for item in tile.items if item.is_food()]) > 0

    def canPickupHeavy(self):
        # for poly and stuff
        return False

    def canOpen(self, tile):
        return not tile.shopkeepDoor and tile.is_door and (tile.locked or self.kernel().hero.legShape) and tile.isAdjacent(self.kernel().curTile())

    def _get_direction(self, source, target):
        if abs(source.y - target.y) > 1 or abs(source.x - target.x) > 1:
            self.kernel().die(f"\n\nAsked for directions to a nonadjacent tile {source} -> {target}\n\n")
        if source.y < target.y and source.x < target.x:
            return 'n'
        if source.y < target.y and source.x == target.x:
            return 'j'
        if source.y < target.y and source.x > target.x:
            return 'b'
        if source.y == target.y and source.x < target.x:
            return 'l'
        if source.y == target.y and source.x > target.x:
            return 'h'
        if source.y > target.y and source.x < target.x:
            return 'u'
        if source.y > target.y and source.x == target.x:
            return 'k'
        if source.y > target.y and source.x > target.x:
            return 'y'
