import numpy as np

from nethack_raph.Actions.base import BaseAction


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

    def execute(self, tile):
        lvl = self.kernel().curLevel()

        if self.hero.isEngulfed:
            targets = list(lvl.adjacent(lvl.tiles[self.hero.coords()]))
            xy = tuple(np.random.choice(targets).xy)
            self.hero.attack(xy)
            return

        monster = lvl.monsters.get(tile)
        if monster and monster.is_attackable:
            self.hero.attack(tile)
        else:
            self.hero.move(tile)
