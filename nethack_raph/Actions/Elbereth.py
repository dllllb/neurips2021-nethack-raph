from nethack_raph.myconstants import DUNGEON_HEIGHT, DUNGEON_WIDTH

import numpy as np


class Elbereth:
    def __init__(self, kernel):
        self.kernel = kernel
        self.read = False

    def can(self):
        if self.kernel().hero.curhp >= self.kernel().hero.maxhp / 2:
            return False, np.zeros((DUNGEON_HEIGHT, DUNGEON_WIDTH))

        if self.kernel().hero.lastAction == 'read' and self.kernel().curTile().has_elbereth:
            self.kernel().log("We are staying on elbereth sign already")
            return False, np.zeros((DUNGEON_HEIGHT, DUNGEON_WIDTH))

        if self.kernel().curTile().char in ['{', '}']:
            # can't write on the fountains
            return False, np.zeros((DUNGEON_HEIGHT, DUNGEON_WIDTH))

        if self.kernel().hero.blind or self.kernel().hero.confused or self.kernel().hero.isEngulfed or self.kernel().hero.isLycanthropy:
            # too hard to write while blinded or confused etc.
            return False, np.zeros((DUNGEON_HEIGHT, DUNGEON_WIDTH))

        neib_monsters = list(filter(
            lambda t: t.monster and t.monster.isAttackable() and not t.monster.respect_elbereth,
            self.kernel().curLevel().tiles
        ))
        if neib_monsters:
            self.kernel().log("Beware, there is a monster nearby, that doesn't respect elbereth")
            return False, np.zeros((DUNGEON_HEIGHT, DUNGEON_WIDTH))

        neib_monsters = list(filter(
            lambda t: t.monster and t.monster.isAttackable(),
            self.kernel().curTile().neighbours()
        ))
        if neib_monsters:
            return True, np.ones((DUNGEON_HEIGHT, DUNGEON_WIDTH))
        else:
            return False, np.zeros((DUNGEON_HEIGHT, DUNGEON_WIDTH))

    def after_search(self, path):
        pass

    def execute(self, path):
        if self.kernel().hero.lastAction != 'read':
            self.kernel().hero.read()
            self.read = True

        else:
            self.kernel().hero.write()
