import numpy as np

from nethack_raph.Actions.base import BaseAction


class RandomWalk(BaseAction):
    def can(self, level):
        return True, None

    def execute(self, path):
        self.kernel().hero.search(1)
