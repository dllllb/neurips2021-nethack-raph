import numpy as np

from nethack_raph.Actions.base import BaseAction
from nethack_raph.Actions.RangeAttackMonster import range_attack_candidates


class CheckTraps(BaseAction):
    def can(self, level):
        if not np.all(level.neighbours.searched):
            return True, None

        return False, None

    def execute(self, path=None):
        self.hero.search(times=1)
