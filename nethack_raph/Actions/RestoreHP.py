from nethack_raph.myconstants import HEIGHT, WIDTH

import numpy as np


class RestoreHP:
    def __init__(self, kernel):
        self.kernel = kernel
        self.has_elbereth = False
        self.read = False

    def can(self):
        # neib_monsters = list(filter(lambda t: t.monster and t.monster.isAttackable(), self.kernel().curTile().neighbours()))
        if self.kernel().hero.curhp < self.kernel().hero.maxhp / 2:
            return True, np.ones((HEIGHT, WIDTH))
        return False, np.zeros((HEIGHT, WIDTH))

    def after_search(self, path):
        pass

    def execute(self, path):
        if not self.read:
            self.kernel().send(':')
            self.read = True
            return

        self.read = False
        # self.has_elbereth is updated by senses when read is executed
        if self.has_elbereth:
            self.kernel().log("Searching for 10 turns because my HP is low")
            self.kernel().hero.search(10)
            self.has_elbereth = False
            return
        # else:
        self.kernel().send('E-')

