from nethack_raph.myconstants import HEIGHT, WIDTH

import numpy as np


class Pray:
    def __init__(self, kernel):
        self.kernel = kernel

    def can(self):
        if self.kernel().hero.hunger < 3:
            # count turns would be better
            self.kernel().hero.god_is_angry = False
            return False, np.zeros((HEIGHT, WIDTH))

        # set by senses
        if self.kernel().hero.god_is_angry:
            return False, np.zeros((HEIGHT, WIDTH))

        return True, np.ones((HEIGHT, WIDTH))

    def after_search(self, path):
        pass

    def execute(self, path):
        self.kernel().send('#pray\ry')
