import time
from nethack_raph.Kernel import *
from nethack_raph.Tile import *
import numpy as np


class AttackMonster:
    def __init__(self):
        self.goal = None
        self.path = None
        self.attack = None

    def can(self):
        if Kernel.instance.Hero.isEngulfed:
            Kernel.instance.log("Attacking while engulfed..")
            self.goal = Kernel.instance.curTile().neighbours()[0]
            self.attack = True
            return True

        # O(n)
        monsters = Kernel.instance.curLevel().findAttackableMonsters()
        Kernel.instance.log(f"We found {len(monsters)} monsters")

        if len(monsters) == 0:
            return False

        # O(n)
        for monster in monsters:
            if Kernel.instance.curTile().isAdjacent(monster):
                Kernel.instance.log("%s is adjacent to me. Attacking.." % monster)
                self.goal = monster
                self.attack = True
                return True

        self.path = None
        candidates = np.zeros((HEIGHT, WIDTH))
        for monster in monsters:
            for neighbour in monster.walkableNeighbours():
                candidates[neighbour.coords()] = True

        # O(dijkastra)
        self.path = Kernel.instance.Pathing.a_star_search(condition_fn=lambda tile: candidates[tile.coords()])

        if self.path:
            Kernel.instance.log("Found monster. Path:(%s)" % str(self.path))
            return True

        return False

    def execute(self):
        if self.attack:
            Kernel.instance.Hero.attack(self.goal)
            self.attack = False
            self.goal = None
            self.path = None
        else:
            Kernel.instance.sendSignal("interrupt_action", self)
            self.path.draw(color=COLOR_BG_RED)
            Kernel.instance.log("Going towards monster")
            Kernel.instance.Hero.move(self.path[1].tile)
