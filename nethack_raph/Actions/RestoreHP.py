from nethack_raph.myconstants import DUNGEON_HEIGHT, DUNGEON_WIDTH

import numpy as np


class RestoreHP:
    def __init__(self, kernel):
        self.kernel = kernel
        self.read = False

    def can(self):
        if self.kernel().hero.curhp >= self.kernel().hero.maxhp / 2:
            return False, np.zeros((DUNGEON_HEIGHT, DUNGEON_WIDTH))

        neib_monsters = list(filter(
            lambda t: t.monster and t.monster.isAttackable(),
            self.kernel().curTile().neighbours()
        ))
        if neib_monsters:
            return False, np.zeros((DUNGEON_HEIGHT, DUNGEON_WIDTH))
        else:
            return True, np.ones((DUNGEON_HEIGHT, DUNGEON_WIDTH))

    def after_search(self, path):
        pass

    def execute(self, path):
        self.kernel().log("Searching for 1 turns because my HP is low")
        self.kernel().hero.search(1)
