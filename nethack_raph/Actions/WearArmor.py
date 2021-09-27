from nethack_raph.myconstants import DUNGEON_HEIGHT, DUNGEON_WIDTH

import numpy as np


class WearArmor:
    def __init__(self, kernel):
        self.kernel = kernel
        self.action_to_do = None

    def can(self):
        if self.kernel().inventory.new_armors:
            self.action_to_do = 'wear'
            return True, np.ones((DUNGEON_HEIGHT, DUNGEON_WIDTH))

        armor_tiles = np.zeros((DUNGEON_HEIGHT, DUNGEON_WIDTH))
        found_armor = False
        for armor in filter(
                lambda t: any([item.item_type == 'armor' for item in t.items]),
                [t for t in self.kernel().curLevel().tiles if not t.dropped_here]):
            armor_tiles[armor.coords()] = True
            found_armor = True
            self.action_to_do = 'pick_up'
            self.kernel().log(f"Found armor {armor}: {list(map(lambda t: str(t), armor.items))}")
        return found_armor, armor_tiles

    def after_search(self, path):
        pass

    def execute(self, path):
        if self.action_to_do == 'wear':
            self.kernel().hero.wear()
            return

        if len(path) == 1:
            assert path[0] == self.kernel().curTile()
            self.kernel().hero.pick()
            return

        self.kernel().log(path)
        self.kernel().hero.move(path[-2])
        # self.kernel().sendSignal("interrupt_action", self)

