from nle.nethack import MAX_GLYPH
from nethack_raph.Item import Item
from nethack_raph.Monster import Monster
from nethack_raph.myconstants import DUNGEON_HEIGHT, DUNGEON_WIDTH

import numpy as np
from collections import defaultdict

dtTile = np.dtype([
    ('xy', np.dtype([    # backreference
        ('x', np.uint8),
        ('y', np.uint8),
    ])),
    ('char', np.dtype('<U1')),       # dungeon char. ansi char in unicode
    ('appearance', np.dtype('<U1')),  # appearance char. ansi char in unicode
    ('glyph', np.int16),      # glyph
    ('walk_cost', float),  # pathfinding cost
    ('explored', bool),
    ('walkable_tile', bool),
    ('walkable_glyph', bool),
    ('is_hero', bool),
    ('is_opened_door', bool),
    ('is_closed_door', bool),
    ('in_shop', bool),
    ('shop_entrance', bool),
    ('searches', int),
    ('searched', bool),
    ('locked', bool),
    ('shopkeep_door', bool),
    ('dropped_here', bool),
    ('has_elbereth', bool),
])


def fold(array, k=1, *, writeable=True):
    d0, d1, *shape = array.shape
    s0, s1, *strides = array.strides

    return np.lib.stride_tricks.as_strided(
        array,
        (d0 - 2 * k, d1 - 2 * k, 1 + 2 * k, 1 + 2 * k, *shape),
        (s0, s1, s0, s1, *strides),
        writeable=writeable,
    )


class Level:
    glyph_ranges = {
        'monster': (0, 380),
        'pet': (381, 761),
        'corpse': (1144, 1524),
        'ridden': (1525, 1905),
        'dungeon': (2359, 2445),
        'item': (1907, 2356),
        'statue': (5595, 5975),
        'invisible monster': (762, 762),
        'mimic': (1906, 1906)
    }
    dngGlyphsToExplore = (
        2359,  # either unexplored or solid stone
        2379,  # dark part of a room
        2380,  # corridor
        2372,  # open door
        2373,  # open door
        2371,  # doorway (with no door)
    )
    walkables = {
        '.': 1,
        '}': 1,
        '{': 1,
        '#': 1,
        '<': 1,
        '>': 1,
        '^': 100,
        ' ': 1
    }
    wereCreaturesGlyphs = (
        15,  # werejackal
        21,  # werewolf
        90,  # wererat
    )

    def log(self, message):
        self.kernel().log(message)

    def __init__(self, kernel, dlvl, height=DUNGEON_HEIGHT, width=DUNGEON_WIDTH):
        # def __init__(self, kernel, dlvl):
        self.kernel = kernel
        self.kernel().log("Making a level")

        self.dlvl = dlvl
        self.branchname = self.kernel().dungeon.curBranch.name
        self.explored = False
        self.maxSearches = 10
        self.kernel().log("Made a Level() with dlvl: %d in branch %s" % (self.dlvl, self.branchname))

        # dense data structures
        # the map data is a bordered level. glyph determines if it is valid
        self.data = data = np.zeros(
            (1 + height + 1, 1 + width + 1),
            dtype=dtTile,
        ).view(np.recarray)
        data.glyph[:] = MAX_GLYPH
        data.walkable_glyph[:] = True
        data.xy[:] = (-1, -1)  # map to the same x-y

        # setup O(1) lookup for adjacent tiles on the bordered map
        self.neighbours = fold(data, 1, writeable=True).view(np.recarray)

        # the level proper
        self.tiles = tiles = data[1:-1, 1:-1]
        for xy in np.ndindex(tiles.shape):
            tiles[xy].xy = xy

        # sparse data structures x-y keys (unbordered coords)
        self.monsters = defaultdict(lambda: None)  # the monster population
        self.items = defaultdict(list)  # sparse table of item piles

    @property
    def shape(self):
        return self.tiles.shape

    def update_one(self, tile, char, glyph):
        # update one tile at the specified location
        x, y = tile.xy

        glyph_type = self.glyph_type(glyph)

        if (x, y) in self.monsters:
            del self.monsters[x, y]

        if glyph_type == 'dungeon':
            tile.char = char
            tile.glyph = glyph
            tile.is_closed_door = glyph in (2374, 2375)
            tile.is_opened_door = tile.is_opened_door or glyph in (2372, 2373)
            tile.explored = tile.explored or glyph not in Level.dngGlyphsToExplore
            self.clear_items(x, y)

            if char not in Level.walkables.keys() and not tile.is_opened_door:
                tile.walkable_glyph = False
            if char in Level.walkables.keys() and char not in [' ']:
                tile.walkable_glyph = True

        elif glyph_type in ('item', 'corpse'):
            if not [item for item in self.items[x, y] if item.glyph == glyph]:
                self.items[x, y].append(Item(None, char, glyph, self.kernel))
                self.log(f'Found item: {(tile.xy, str(self.items[x, y][-1]))}')
            if char == '0':
                tile.walkable_glyph = char != '0'

        elif glyph_type in ('monster', 'pet', 'invisible monster') and tuple(tile.xy) != self.kernel().hero.coords():
            self.monsters[x, y] = Monster(char, glyph, self.kernel)
            self.log(f'Found monster: {(tile.xy, str(self.monsters[x, y]))}')
            tile.walkable_glyph = True
            if tile.char == '+':  # The door is open
                self.set_as_door(tile)

        self.update_walk_cost(tile)

    def clear_items(self, x, y):
        if (x, y) in self.items: del self.items[x, y]

    def update_hero(self, glyph):
        self.tiles.is_hero[:] = False
        tile = self.tiles[self.kernel().hero.coords()]
        tile.is_hero = True
        tile.explored = True
        tile.walkable_glyph = True
        self.update_walk_cost(tile)
        self.kernel().hero.isLycanthropy = glyph in Level.wereCreaturesGlyphs

    def set_as_door(self, tile):
        tile.is_opened_door = True
        tile.is_closed_door = False
        tile.char = '-'
        tile.glyph = 2373
        self.update_walk_cost(tile)

    def get_neighbours(self, tile):
        return [t for t in self.neighbours[tuple(tile.xy)].reshape(-1) if t.xy.x < 255 and t.xy.y < 255]

    def set_as_trap(self, tile):
        tile.char = '^'
        self.update_walk_cost(tile)

    def update_walk_cost(self, tile):
        x, y = tile.xy

        if tile.shop_entrance:  # TODO: Shops might be good to visit sometime
            tile.walkable_tile = False
        elif not tile.char:
            tile.walkable_tile = tile.walkable_glyph
        else:
            tile.walkable_tile = (tile.char in Level.walkables.keys() and tile.walkable_glyph) or tile.is_opened_door

        tile.walk_cost = float('inf')
        if tile.walkable_tile:
            tile.walk_cost = Level.walkables.get(tile.char, 1)
            if (x, y) in self.monsters and not self.monsters[x, y].pet:
                tile.walk_cost += 100

    def update(self, chars, glyphs):
        hero = self.kernel().hero
        tiles = self.tiles

        chars = np.array([chars.translate({
            ord('`'): '0',
        })]).view('<U1').reshape(tiles.shape)

        xy = (tiles.appearance != chars).nonzero()
        # xy is relative to the view area (.tiles)

        # BULK COPY: reinterprete and copy ('no' raises if anything goes bad)
        np.copyto(tiles.appearance, chars, 'no')

        for pt in zip(*xy):
            tile, char, gly = tiles[pt], chars[pt], glyphs[pt]
            self.update_one(tile, char, gly)
            if tuple(tile.xy) != hero.coords():
                self.explored = False

        neighbours = self.neighbours[hero.coords()]
        neighbours = neighbours[(neighbours.appearance == ' ') & neighbours.walkable_glyph].xy
        for x, y in neighbours:
            if x == 255 or y == 255: continue
            tile = self.tiles[x, y]
            tile.walkable_glyph = False
            self.update_walk_cost(tile)

        self.update_hero(glyphs[hero.coords()])

    @staticmethod
    def glyph_type(glyph):
        for name, (left, right) in Level.glyph_ranges.items():
            if left <= glyph <= right:
                return name
