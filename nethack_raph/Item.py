from nethack_raph.Findable import *


class Item(Findable):
    CURSED = 0
    UNCURSED = 1
    BLESSED = 2
    UNKNOWNBUC = 3

    def __init__(self, name, char, color, glyph, kernel, heavy=False):
        Findable.__init__(self)

        self.name = name
        self.qty = 1
        self.enchants = 0
        self.buc = Item.UNKNOWNBUC

        self.slot = None
        self.page = None

        self.char = char
        self.color = color
        self.heavy = heavy or self.char in ['0']

        self.glyph = glyph
        self.kernel = kernel

    def __str__(self):
        return "?:%s, ch:%s, c:%s, g:%s" % tuple(map(str, (self.name, self.char, self.color, self.glyph)))

    def isHeavy(self):
        return self.char in ['`', '0']

    def canPickup(self):
        return self.char not in ['_', '\\']

    def identified(self, id):
        self.name = id

    def is_food(self):
        return self.char == '%' and self.name != 'corpse'
