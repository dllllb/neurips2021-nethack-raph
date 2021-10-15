import numpy as np

from nethack_raph.Actions.base import BaseAction


class Pray(BaseAction):
    last_pray_turn, timeout = -1000, 800

    def can(self, level):
        if self.hero.turns - self.last_pray_turn < self.timeout:
            return False, None

        hero = self.hero
        if hero.hunger >= 3 or hero.isLycanthropy or hero.curhp <= 5 or \
                hero.curhp <= hero.maxhp / 7 or hero.levitating_curse:
            return True, None

        return False, None

    def execute(self, path=None):
        assert path is None

        self.last_pray_turn = self.hero.turns
        self.hero.pray()
