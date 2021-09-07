from nethack_raph.myconstants import HEIGHT, WIDTH

import numpy as np


class RandomWalk:
    def __init__(self, kernel):
        self.kernel = kernel

    def can(self):
        return True, np.ones((HEIGHT, WIDTH))

    def after_search(self, path):
        pass

    def execute(self, path):
        self.kernel().hero.search()
