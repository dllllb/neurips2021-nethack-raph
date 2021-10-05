import numpy as np

from nethack_raph.Actions.base import BaseAction
from nethack_raph.myconstants import COLOR_BG_RED


class AttackMonster(BaseAction):
    def can(self, level):
        monsters = np.zeros(level.shape, dtype=bool)
        if self.hero.isEngulfed:
            monsters[:] = True
            self.log("Attacking while engulfed..")

        else:
            for xy, m in level.monsters.items():
                if m.is_attackable:
                    monsters[xy] = True
                    self.log(f"Found monster {xy}: {str(m)}")

        return monsters.any(), monsters

    def execute(self, path):
        self.log(f'len path: {len(path)}')
        if self.hero.isEngulfed:
            self.hero.attack((self.hero.x + 1, self.hero.y))
            return

        mon, *middle, one = path
        if middle:
            self.log("Going towards monster")
            self.draw_path(path, color=COLOR_BG_RED)
            self.hero.move(middle[-1])
            return

        # we are next to the monster
        self.hero.attack(mon)
