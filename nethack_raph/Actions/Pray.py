from nethack_raph.myconstants import HEIGHT, WIDTH

import numpy as np


class Pray:
    def __init__(self, kernel):
        self.kernel = kernel
        self.prev_pray = -1000

    def can(self):
        if self.kernel().hero.turns - self.prev_pray < 1000:
            return False, np.zeros((HEIGHT, WIDTH))

        if self.kernel().hero.hunger < 3 and self.kernel().hero.curhp > 6:
            return False, np.zeros((HEIGHT, WIDTH))

        return True, np.ones((HEIGHT, WIDTH))

    def after_search(self, path):
        pass

    def execute(self, path):
        self.prev_pray = self.kernel().hero.turns
        self.kernel().send('#pray\ry')
