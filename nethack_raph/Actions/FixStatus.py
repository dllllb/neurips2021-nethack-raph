from nethack_raph.Kernel import *
import numpy as np


class FixStatus:
    def __init__(self):
        pass

    def can(self):
        if Kernel.instance.Hero.blind or Kernel.instance.Hero.isPolymorphed:
            return True, np.ones((HEIGHT, WIDTH))
        return False, np.zeros((HEIGHT, WIDTH))

    def after_search(self, path):
        pass

    def execute(self, path):
        Kernel.instance.Hero.search(5)
