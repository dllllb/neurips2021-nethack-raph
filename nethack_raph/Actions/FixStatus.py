from nethack_raph.myconstants import DUNGEON_HEIGHT, DUNGEON_WIDTH

import numpy as np


class FixStatus:
    def __init__(self, kernel):
        self.kernel = kernel

    def can(self):
        if self.kernel().hero.blind or self.kernel().hero.isPolymorphed:
            return True, np.ones((DUNGEON_HEIGHT, DUNGEON_WIDTH))
        return False, np.zeros((DUNGEON_HEIGHT, DUNGEON_WIDTH))

    def after_search(self, path):
        pass

    def execute(self, path):
        self.kernel().hero.search(5)
