import numpy as np

from nethack_raph.Actions.base import BaseAction


class UseItem(BaseAction):
    def can(self, level):
        return False, None

    def execute(self, path=None):
        pass
