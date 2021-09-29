from nethack_raph.Item import *
from nethack_raph.Monster import *
from nethack_raph.TermColor import *
from nethack_raph.Findable import *

import numpy as np


def calc_neighbours():
    offset = np.array(((-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)), dtype=np.int)
    result = []
    for y in range(DUNGEON_HEIGHT):
        result.append([])
        for x in range(DUNGEON_WIDTH):
            coords = (np.array(((y, x),), dtype=np.int) + offset).T
            (ids,) = np.where(
                (coords[0] < DUNGEON_HEIGHT) &
                (coords[0] >= 0) &
                (coords[1] < DUNGEON_WIDTH) &
                (coords[1] >= 0)
            )
            result[y].append(coords[1][ids] + coords[0][ids] * DUNGEON_WIDTH)
    return result


_NEIGHBOURS = calc_neighbours()


class Tile(Findable):
    dngFeatures = ['.', '}', '{', '#', '<', '>', '+', '^', '|', '-', '~', ' ']
    dngItems    = ['`', '0', '*', '$', '_', '[', '%', ')', '(', '/', '?', '!', '"', '=', '+', '\\']
    dngMonsters = list(map(chr, range(ord('a'), ord('z')+1))) + \
                  list(map(chr, range(ord('A'), ord('Z')+1))) + \
                  list(map(chr, range(ord('1'), ord('5')+1))) + \
                        ['@', "'", '&', ';', ':']
    walkables    = {'.': 1,
                    '}': 1,
                    '{': 1,
                    '#': 1,
                    '<': 1,
                    '>': 1,
                    '^': 100,
                    ' ': 1}  #char: weight

    dngGlyphsToExplore = (
        2359,  # either unexplored or solid stone
        2379,  # dark part of a room
        2380,  # corridor
        2372,  # open door
        2373,  # open door
        2371,  # doorway (with no door)
    )
    wereCreaturesGlyphs = (
        15,  # werejackal
        21,  # werewolf
        90,  # wererat
    )

    def __init__(self, y, x, level, kernel):
        Findable.__init__(self)
        self.kernel = kernel

        self.y = y
        self.x = x
        self.level = level

        self.char = None
        self.color = TermColor()

        self.explored = False
        self.items = []
        self.monster = None

        self.walkable_glyph = True
        self.walkable_tile = False

        self.searches = 0
        self.searched = False

        self.inShop = False
        self.walk_cost = 1

        self.locked = False
        self.shopkeepDoor = False
        self.is_closed_door = False
        self.is_opened_door = False
        self.dropped_here = False
        self.shop_entrance = False

        self.has_elbereth = False
        self.kernel = kernel

    def coords(self):
        return self.y, self.x

    def setTile(self, char, color, glyph):
        self.monster = None

        # closed door and locked door
        self.is_closed_door = glyph in (2374, 2375)
        self.is_opened_door = self.is_opened_door or glyph in (2372, 2373)

        # fix for mimic monster
        char = 'm' if char == ']' else char
        char = '0' if char == '`' else char # make boulder notisable

        if char in Tile.dngFeatures:
            self.char = char
            self.color = color
            self.glyph = glyph

            self.explored = self.explored or glyph not in Tile.dngGlyphsToExplore

            if self.items:
                self.kernel().log("Removing items on %s because I only see a dngFeature-tile" % str(self.coords()))
                self.items = []

            if char not in Tile.walkables.keys() and not self.is_opened_door:
                self.kernel().log("Setting %s to unwalkable." % self)
                self.walkable_glyph = False
            if char in Tile.walkables.keys() and char not in [' ']:
                self.walkable_glyph = True

        elif char in Tile.dngItems:
            it = Item(None, char, color, glyph, self.kernel)
            if not self.items:
                self.kernel().log("Added item(%s) to tile(%s)" % (str(it), str(self)))
                self.items.append(it)
            else:
                self.items[0] = it

            if char == '0':
                self.walkable_glyph = False
            else:
                self.walkable_glyph = True

        elif self.coords() == self.kernel().curTile().coords():
            self.explored = True
            self.walkable_glyph = True
            self.kernel().hero.isLycanthropy = glyph in Tile.wereCreaturesGlyphs

            # Might cause some trouble
            # TODO: Write comments that actually explains problems (No idea why I said the above, and no idea what the below does.. :) 
            if not self.walkable_tile:
                self.walkable_glyph = True
                self.char = None

        elif char in Tile.dngMonsters:
            self.monster = Monster(char, color, glyph, self.kernel)
            self.walkable_glyph = True
            if self.char == '+':  # The door is open
                self.setTile('-', TermColor(33, 0, False, False), 2373)

        else:
            self.char = char
            # self.kernel().die("Couldn't parse tile: " + char)

        self.update_walk_cost()
        self.update_is_walkable()

    def update_walk_cost(self):
        walk_cost = Tile.walkables.get(self.char, 1)
        if self.monster and not self.monster.pet:
            walk_cost += 100
        self.walk_cost = walk_cost

    def set_as_trap(self):
        self.char = '^'
        self.update_walk_cost()

    def appearance(self):
        if self.monster:
            return self.monster.char
        elif self.items:
            return self.items[-1].char
        else:
            return self.char

    # def isDoor(self):
    #     return (self.char == '-' or self.char == '|') and self.color.getId() == COLOR_BROWN

    def update_is_walkable(self): #TODO: Shops might be good to visit sometime ..:)
        if self.shop_entrance:
            self.walkable_tile = False

        elif not self.char:
            self.walkable_tile = self.walkable_glyph

        else:
            self.walkable_tile = (self.char in Tile.walkables.keys() and self.walkable_glyph) or self.is_opened_door

    def walkableNeighbours(self):
        ret = []

        for neighbour in self.neighbours():
            if neighbour.walkable_tile and not (neighbour.is_opened_door or self.is_opened_door):
                ret.append(neighbour)
                continue
            if (self.is_opened_door or neighbour.is_opened_door) and (self.x == neighbour.x or self.y == neighbour.y) and neighbour.walkable_tile:
                ret.append(neighbour)
                continue
        return ret

    def isAdjacent(self, other):
        for neighbour in self.neighbours():
            if neighbour == other:
                return True
        return False

    def straight(self, find=None):
        ret = []
        for x, y in ((-1, 0), (1, 0), (0, -1), (0, 1)):
            if x + self.x < 0 or x + self.x >= DUNGEON_WIDTH or y + self.y < 0 or y + self.y >= DUNGEON_HEIGHT:
                continue
            tile = self.level.tiles[(x + self.x) + (y + self.y) * DUNGEON_WIDTH]
            if find is None or tile.find(find):
                ret.append(tile)
        return ret

    def adjacent(self, find):
        return [tile for tile in self.neighbours() if tile.find(find)]

    def neighbours(self):
        return self.level.tiles[_NEIGHBOURS[self.y][self.x]]

    def isHero(self):
        return self.coords() == self.kernel().curTile().coords()

    def tilesFromCurrent(self):
        return abs(self.kernel().hero.x - self.x) + abs(self.kernel().hero.y - self.y)

    def __str__(self):
        return "(%s,%s)->g:%s, c:(%s), e:%s, @:%s, m:(%s), i:(%s) w:%s(is:%s) sea:%s" % tuple(map(str, (self.y, self.x, self.char, self.color, self.explored, self.isHero(), self.monster, map(str, self.items), self.walkable_glyph, self.walkable_tile, self.searches)))

    def __eq__(self, other):
        return self.coords() == other.coords()

    def __ne__(self, other):
        return self.coords() != other.coords()
