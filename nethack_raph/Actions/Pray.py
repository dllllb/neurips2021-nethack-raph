import numpy as np

from nethack_raph.Actions.base import BaseAction


class Pray(BaseAction):
    last_pray_turn, timeout = -1000, 1000

    def can(self, level):
        if self.hero.turns - self.last_pray_turn < self.timeout:
            return False, np.zeros(level.shape, dtype=bool)

        hero = self.hero
        if hero.hunger >= 3 or hero.isLycanthropy or hero.curhp <= 5 or hero.curhp <= hero.maxhp / 7:
            return True, np.ones(level.shape, dtype=bool)

        return False, np.zeros(level.shape, dtype=bool)

    def execute(self, path):
        self.last_pray_turn = self.hero.turns
        self.hero.pray()
