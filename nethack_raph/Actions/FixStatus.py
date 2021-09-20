from nethack_raph.myconstants import HEIGHT, WIDTH

import numpy as np


class FixStatus:
    def __init__(self, kernel):
        self.kernel = kernel

    def can(self):
        if self.kernel().hero.blind or self.kernel().hero.isLycanthropy:
            return True, np.ones((HEIGHT, WIDTH))
        return False, np.zeros((HEIGHT, WIDTH))

    def after_search(self, path):
        pass

    def execute(self, path):
        self.kernel().hero.search(5)
