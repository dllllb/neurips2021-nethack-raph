from nethack_raph.Tile import *
import numpy as np


class AttackMonster:
    def __init__(self, kernel):
        self.kernel = kernel

    def can(self):
        if self.kernel().hero.isEngulfed:
            self.kernel().log("Attacking while engulfed..")
            return True, np.ones((DUNGEON_HEIGHT, DUNGEON_WIDTH))


        # O(n)
        monsters = self.kernel().curLevel().findAttackableMonsters()
        self.kernel().log(f"We found {len(monsters)} monsters")
        target_tiles = np.zeros((DUNGEON_HEIGHT, DUNGEON_WIDTH))

        # O(n)
        found_monsters = False
        for monster in monsters:
            self.kernel().log(f'monster: {monster}, self: {self.kernel().curTile()}')
            for neighbour in monster.walkableNeighbours():
                target_tiles[neighbour.coords()] = True
                found_monsters = True
        return found_monsters, target_tiles

    def after_search(self, path):
        pass

    def execute(self, path):
        self.kernel().log(f'len path: {len(path)}')
        if len(path) == 1:
            assert path[0] == self.kernel().curTile()
            for tile in self.kernel().curTile().neighbours():
                if tile.monster and tile.monster.isAttackable():
                    self.kernel().hero.attack(tile)
                    return
            self.kernel().log('monster is absent')
            self.kernel().send(' ')
            return

        self.kernel().sendSignal("interrupt_action", self)
        self.kernel().draw_path(path, color=COLOR_BG_RED)
        self.kernel().log("Going towards monster")
        self.kernel().hero.move(path[-2])
