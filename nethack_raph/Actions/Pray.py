from nethack_raph.myconstants import DUNGEON_HEIGHT, DUNGEON_WIDTH

import numpy as np


class Pray:
    def __init__(self, kernel):
        self.kernel = kernel
        self.prev_pray = -1000

    def can(self, level):
        if self.kernel().hero.turns - self.prev_pray < 1000:
            return False, np.zeros((DUNGEON_HEIGHT, DUNGEON_WIDTH))

        hero = self.kernel().hero
        if hero.hunger >= 3 or hero.curhp <= 5 or hero.isLycanthropy or hero.curhp <= hero.maxhp / 7:
            return True, np.ones((DUNGEON_HEIGHT, DUNGEON_WIDTH))

        return False, np.zeros((DUNGEON_HEIGHT, DUNGEON_WIDTH))

    def after_search(self, path):
        pass

    def execute(self, path):
        self.prev_pray = self.kernel().hero.turns
        self.kernel().hero.pray()
