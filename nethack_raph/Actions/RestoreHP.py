from nethack_raph.myconstants import HEIGHT, WIDTH

import numpy as np


class RestoreHP:
    def __init__(self, kernel):
        self.kernel = kernel

    def can(self):
        if self.kernel().hero.curhp <= (self.kernel().hero.maxhp/2):
            return True, np.ones((HEIGHT, WIDTH))
        return False, np.zeros((HEIGHT, WIDTH))

    def after_search(self, path):
        pass

    def execute(self, path):
        self.kernel().log("Searching for 10 turns becuase my HP is low")
        self.kernel().hero.search(10)
