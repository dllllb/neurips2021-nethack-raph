import numpy as np

from nethack_raph.Actions.base import BaseAction


class FixStatus(BaseAction):
    def can(self, level):
        if self.hero.blind or self.hero.isLycanthropy:
            return True, np.ones(level.shape, dtype=bool)

        return False, np.zeros(level.shape, dtype=bool)

    def execute(self, path):
        # XXX what is five?
        self.hero.search(5)
