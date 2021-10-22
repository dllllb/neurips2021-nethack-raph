import numpy as np

from nethack_raph.Actions.base import BaseAction
from nethack_raph.myconstants import COLOR_BG_RED


class AttackMonster(BaseAction):
    def can(self, level):
        monsters = np.zeros(level.shape, dtype=bool)
        currx, curry = self.kernel().hero.coords()

        if self.hero.isEngulfed:
            monsters[:] = True
            monsters[(currx, curry)] = False
            self.log("Attacking while engulfed..")
            return True, monsters


        def dist_form_current(xy):
            tx, ty = xy
            return abs(tx - currx) + abs(ty - curry)

        for xy, m in level.monsters.items():
            if m.is_attackable and dist_form_current(xy) < 5:
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
