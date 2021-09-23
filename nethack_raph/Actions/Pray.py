from nethack_raph.myconstants import DUNGEON_HEIGHT, DUNGEON_WIDTH

import numpy as np


class Pray:
    def __init__(self, kernel):
        self.kernel = kernel
        self.prev_pray = -1000

    def can(self):
        if self.kernel().hero.turns - self.prev_pray < 1000:
            return False, np.zeros((DUNGEON_HEIGHT, DUNGEON_WIDTH))

        if self.kernel().hero.hunger < 3 and self.kernel().hero.curhp > 6 and not self.kernel().hero.isLycanthropy:
            return False, np.zeros((DUNGEON_HEIGHT, DUNGEON_WIDTH))

        return True, np.ones((DUNGEON_HEIGHT, DUNGEON_WIDTH))

    def after_search(self, path):
        pass

    def execute(self, path):
        self.prev_pray = self.kernel().hero.turns
        self.kernel().hero.pray()
