from nethack_raph.Findable import *
from nethack_raph.MonsterGlossary import MONSTERS_GLOSSARY


class Item(Findable):
    CURSED = 0
    UNCURSED = 1
    BLESSED = 2
    UNKNOWNBUC = 3

    bad_effects = ['mimic', 'poisonous', 'hallucination', 'stun', 'die', 'acidic', 'lycanthropy', 'slime',
                   'petrify', 'aggravate']

    ambivalent_effects = ['speed toggle']  # can be either good or bad, depending on the circumstances

    good_effects = ['cure stoning', 'reduce confusion', 'reduce stunning',
                    'heal', 'cold resistance', 'disintegration resistance', 'fire resistance',
                    'poison resistance', 'shock resistance', 'sleep resistance', 'gain level',
                    'teleport control', 'gain telepathy', 'increase intelligence', 'polymorphing',
                    'increase strength', 'increase energy', 'teleportitis', 'invisibility'
                    ]

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
        self.is_food = self.check_if_food()

        self.corpse = False
        self.turn_of_death = -1000

    def __str__(self):
        return "?:%s, ch:%s, c:%s, g:%s" % tuple(map(str, (self.name, self.char, self.color, self.glyph)))

    def isHeavy(self):
        return self.char in ['`', '0']

    def canPickup(self):
        return self.char not in ['_', '\\']

    def identified(self, id):
        self.name = id

    def check_if_food(self):
        if self.char != '%': return False
        if 1144 <= self.glyph <= 1524:  # corpse
            self.corpse = True
            return False
            monster_corpse = MONSTERS_GLOSSARY[self.glyph - 1144]['corpse']

            if self.kernel().hero.race == monster_corpse['cannibal']:  # cannibalism
                self.kernel().log("%s is not an edible corpse." % self)
                return False

            if any([key in monster_corpse for key in Item.bad_effects + Item.ambivalent_effects]):
                self.kernel().log("%s is not an edible corpse." % self)
                return False

            else:
                self.kernel().log("%s is an edible corpse." % self)
                return True
        else:
            self.kernel().log("%s is food" % self)
            return True

    def is_tainted(self):
        tainted = self.corpse and self.kernel().hero.turns - self.turn_of_death >= 30
        if tainted: self.kernel().log("%s is tainted" % self)
        return tainted
