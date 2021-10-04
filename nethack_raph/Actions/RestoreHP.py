from nethack_raph.myconstants import DUNGEON_HEIGHT, DUNGEON_WIDTH

import numpy as np


class RestoreHP:
    def __init__(self, kernel):
        self.kernel = kernel

    def can(self, level):
        # hp is at an acceptable level
        if self.kernel().hero.curhp >= self.kernel().hero.maxhp / 2:
            return False, np.zeros((DUNGEON_HEIGHT, DUNGEON_WIDTH))

        # monsters nearby
        neib_monsters = list(filter(
            lambda xy: level.monsters[tuple(xy)] is not None and level.monsters[tuple(xy)].is_attackable,
            level.neighbours[level.tiles.is_hero].xy.reshape(-1)
        ))
        if neib_monsters:
            return False, np.zeros((DUNGEON_HEIGHT, DUNGEON_WIDTH))

        # monsters with range attack
        neib_monsters = list(filter(
            lambda m: m is not None and m.is_attackable and m.range_attack,
            level.monsters.values()
        ))
        if neib_monsters:
            return False, np.zeros((DUNGEON_HEIGHT, DUNGEON_WIDTH))

        return True, np.ones((DUNGEON_HEIGHT, DUNGEON_WIDTH))

    def after_search(self, path):
        pass

    def execute(self, path):
        self.kernel().log("Searching for 1 turns because my HP is low")
        self.kernel().hero.search(1)
