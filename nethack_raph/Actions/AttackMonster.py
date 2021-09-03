from nethack_raph.Kernel import *
from nethack_raph.Tile import *
import numpy as np


class AttackMonster:
    def __init__(self):
        pass

    def can(self):
        if Kernel.instance.Hero.isEngulfed:
            Kernel.instance.log("Attacking while engulfed..")
            return True, np.ones((HEIGHT, WIDTH))


        # O(n)
        monsters = Kernel.instance.curLevel().findAttackableMonsters()
        Kernel.instance.log(f"We found {len(monsters)} monsters")
        target_tiles = np.zeros((HEIGHT, WIDTH))

        # O(n)
        found_monsters = False
        for monster in monsters:
            Kernel.instance.log(f'monster: {monster}, self: {Kernel.instance.curTile()}')
            for neighbour in monster.walkableNeighbours():
                target_tiles[neighbour.coords()] = True
                found_monsters = True
        return found_monsters, target_tiles

    def after_search(self, path):
        pass

    def execute(self, path):
        Kernel.instance.log(f'len path: {len(path)}')
        if len(path) == 1:
            assert path.tile == Kernel.instance.curTile()
            for tile in Kernel.instance.curTile().neighbours():
                if tile.monster and tile.monster.isAttackable():
                    Kernel.instance.Hero.attack(tile)
                    return
            Kernel.instance.log('monster is absent')
            Kernel.instance.send(' ')
            return

        Kernel.instance.sendSignal("interrupt_action", self)
        path.draw(color=COLOR_BG_RED)
        Kernel.instance.log("Going towards monster")
        Kernel.instance.Hero.move(path[1].tile)
