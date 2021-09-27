from nethack_raph.Tile import *
import numpy as np


class Level:
    def __init__(self, kernel, dlvl):
        self.kernel = kernel
        self.kernel().log("Making a level")

        self.dlvl = dlvl
        self.branchname = self.kernel().dungeon.curBranch.name
        self.tiles = []
        self.special = None
        self.explored = False
        self.maxSearches = 10

        self.tiles = np.array([Tile(y, x, self, kernel) for y in range(DUNGEON_HEIGHT) for x in range(DUNGEON_WIDTH)])

        self.kernel().log("Made a Level() with dlvl: %d in branch %s" % (self.dlvl, self.branchname))

    def find(self, args):
        return [tile for tile in self.tiles if tile.find(args)]

    def findAttackableMonsters(self):
        return [tile for tile in self.tiles if tile.monster and tile.monster.is_attackable]

    def findUnidentifiedItems(self):
        ret = []
        for tile in self.tiles:
            if tile.items:
                if [item for item in tile.items if not item.appearance]:
                    ret.append(tile)
        return ret

    def findDoors(self):
        return [tile for tile in self.tiles if tile.is_door and not tile.shopkeepDoor]

    def find_food(self):
        return [tile for tile in self.tiles for item in tile.items if item.is_food and not item.is_tainted()]

    def find(self, query):
        return [tile for tile in self.tiles if tile.find(query)]

    def update(self, chars, colors, glyphs):
        for x in range(0, len(self.tiles)):
            char = chars[x]
            glyph = glyphs[x]
            if self.tiles[x].appearance() != char:

                color = 30 + (colors[x] & ~TTY_BRIGHT)
                is_bold = bool(color & TTY_BRIGHT)
                color = TermColor(color, bold=is_bold)

                # tmp = self.tiles[x].appearance()
                # self.kernel().log("\n   <--- %s\n   ---> %s" % (str(self.tiles[x].appearance()), str(char)))
                self.tiles[x].setTile(char, color, glyph)
                if not (self.tiles[x].isHero()):
                    # self.kernel().log("\n   <!!! %s(%s)\n   !!!> %s" % (tmp, str(self.tiles[x].coords()), str(char)))
                    self.explored = False

        for tile in self.kernel().curTile().neighbours():
            if tile.appearance() == ' ' and tile.walkable:
                # self.kernel().log("Setting walkable to False because I think this is rock (%s)" % tile)
                tile.walkable = False
