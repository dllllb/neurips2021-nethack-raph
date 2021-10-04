from nethack_raph.myconstants import DUNGEON_HEIGHT, DUNGEON_WIDTH, COLOR_BG_RED
import numpy as np


class AttackMonster:
    def __init__(self, kernel):
        self.kernel = kernel

    def can(self, level):
        if self.kernel().hero.isEngulfed:
            self.kernel().log("Attacking while engulfed..")
            return True, np.ones((DUNGEON_HEIGHT, DUNGEON_WIDTH))

        monsters = np.zeros((DUNGEON_HEIGHT, DUNGEON_WIDTH))
        for xy, monster in level.monsters.items():
            if monster is not None and monster.is_attackable:
                monsters[xy] = True
                self.kernel().log(f"Found monster {xy}: {str(monster)}")

        return monsters.sum() > 0, monsters

    def after_search(self, path):
        pass

    def execute(self, path):
        self.kernel().log(f'len path: {len(path)}')

        if self.kernel().hero.isEngulfed:
            self.kernel().hero.attack((self.kernel().hero.x + 1, self.kernel().hero.y))
            return

        if len(path) == 2:  # we are next to the monster
            self.kernel().hero.attack(path[-2])
            return

        self.kernel().draw_path(path, color=COLOR_BG_RED)
        self.kernel().log("Going towards monster")
        self.kernel().hero.move(path[-2])
