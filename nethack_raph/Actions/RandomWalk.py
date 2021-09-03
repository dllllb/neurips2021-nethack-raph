from nethack_raph.Kernel import *
import numpy as np


class RandomWalk:
    def __init__(self):
        pass

    def can(self):
        return True, np.ones((HEIGHT, WIDTH))

    def after_search(self, path):
        pass

    def execute(self, path):
        Kernel.instance.Hero.search()
