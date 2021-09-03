from nethack_raph.Kernel import *
import numpy as np


class RestoreHP:
    def __init__(self):
        pass

    def can(self):
        if Kernel.instance.Hero.curhp <= (Kernel.instance.Hero.maxhp/2):
            return True, np.ones((HEIGHT, WIDTH))
        return False, np.zeros((HEIGHT, WIDTH))

    def after_search(self, path):
        pass

    def execute(self, path):
        Kernel.instance.log("Searching for 10 turns becuase my HP is low")
        Kernel.instance.Hero.search(10)
