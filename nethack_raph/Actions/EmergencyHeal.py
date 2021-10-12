import numpy as np

from nethack_raph.Actions.base import BaseAction


class EmergencyHeal(BaseAction):
    def can(self, level):
        if self.hero.curhp >= self.hero.maxhp / 3:
            return False, None

        if self.hero.role == 'hea' and self.hero.curpw > 4:
            return True, None
        
        return False, None

    def execute(self, path=None):
        self.hero.cast_spell('a')
