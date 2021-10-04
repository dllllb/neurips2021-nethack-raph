from nethack_raph.myconstants import DUNGEON_HEIGHT, DUNGEON_WIDTH

import numpy as np


class Elbereth:
    def __init__(self, kernel):
        self.kernel = kernel

    def can(self, level):
        # hp is at an acceptable level
        if self.kernel().hero.curhp >= self.kernel().hero.maxhp / 2:
            return False, np.zeros((DUNGEON_HEIGHT, DUNGEON_WIDTH))

        # we are staying on elbereth sign already
        if self.kernel().hero.lastAction == 'read' and self.kernel().curTile().has_elbereth:
            self.kernel().log("We are staying on elbereth sign already")
            return False, np.zeros((DUNGEON_HEIGHT, DUNGEON_WIDTH))

        # can't write on the fountains
        if self.kernel().curTile().char in ['{', '}']:
            return False, np.zeros((DUNGEON_HEIGHT, DUNGEON_WIDTH))

        # too hard to write while blinded / confused /stun, etc.
        if any([self.kernel().hero.blind,
                self.kernel().hero.confused,
                self.kernel().hero.stun,
                self.kernel().hero.hallu,
                self.kernel().hero.levitating,
                self.kernel().hero.isEngulfed,
                self.kernel().hero.isLycanthropy]):
            return False, np.zeros((DUNGEON_HEIGHT, DUNGEON_WIDTH))

        # monsters with elbereth disrespect or range attack
        neib_monsters = list(filter(
            lambda m: m is not None and m.is_attackable and (not m.respect_elbereth or m.range_attack),
            level.monsters.values()
        ))
        if neib_monsters:
            self.kernel().log("Beware, there is a monster with elbereth disrespect or range attack")
            return False, np.zeros((DUNGEON_HEIGHT, DUNGEON_WIDTH))

        return True, np.ones((DUNGEON_HEIGHT, DUNGEON_WIDTH))

    def after_search(self, path):
        pass

    def execute(self, path):
        if self.kernel().hero.lastAction != 'read':
            self.kernel().hero.read()

        else:
            self.kernel().hero.write()
