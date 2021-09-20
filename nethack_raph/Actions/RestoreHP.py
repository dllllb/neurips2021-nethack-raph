from nethack_raph.myconstants import HEIGHT, WIDTH

import numpy as np


class RestoreHP:
    def __init__(self, kernel):
        self.kernel = kernel
        self.read = False

    def can(self):
        # neib_monsters = list(filter(lambda t: t.monster and t.monster.isAttackable(), self.kernel().curTile().neighbours()))
        if self.kernel().hero.curhp < self.kernel().hero.maxhp / 2:
            return True, np.ones((HEIGHT, WIDTH))
        return False, np.zeros((HEIGHT, WIDTH))

    def after_search(self, path):
        pass

    def execute(self, path):
        if self.kernel().hero.lastAction != 'read':
            self.kernel().hero.read()
            self.read = True

        elif self.kernel().curTile().has_elbereth:
            self.kernel().log("Searching for 1 turns because my HP is low")
            self.kernel().hero.search(1)

        else:
            self.kernel().hero.write()
