from nethack_raph.myconstants import DUNGEON_HEIGHT, DUNGEON_WIDTH

import numpy as np


class PickUpStuff:
    def __init__(self, kernel):
        self.kernel = kernel
        self.action_to_do = None

    def can(self):
        if self.kernel().inventory.take_off_armors:
            self.action_to_do = 'take_off'
            return True, np.ones((DUNGEON_HEIGHT, DUNGEON_WIDTH))

        if self.kernel().inventory.new_armors:
            self.action_to_do = 'wear'
            return True, np.ones((DUNGEON_HEIGHT, DUNGEON_WIDTH))

        armor_tiles = np.zeros((DUNGEON_HEIGHT, DUNGEON_WIDTH))
        found_armor = False
        for armor in filter(
                lambda t: any([item.item_type in ('armor', 'gold_piece') for item in t.items]),
                [t for t in self.kernel().curLevel().tiles if not t.dropped_here and not t.inShop]):
            armor_tiles[armor.coords()] = True
            found_armor = True
            self.action_to_do = 'pick_up'
            self.kernel().log(f"Found armor {armor}: {list(map(lambda t: str(t), armor.items))}")
        return found_armor, armor_tiles

    def after_search(self, path):
        pass

    def execute(self, path):
        if self.action_to_do == 'wear':
            _, _, armor_letter = self.kernel().inventory.new_armors.pop(0)
            self.kernel().hero.wear(armor_letter)
            return

        if self.action_to_do == 'take_off':
            armor_letter = self.kernel().inventory.take_off_armors.pop(0)
            self.kernel().hero.take_off(armor_letter)
            return

        if len(path) == 1:
            assert path[0] == self.kernel().curTile()
            self.kernel().hero.pick()
            return

        self.kernel().log(path)
        self.kernel().hero.move(path[-2])
        # self.kernel().sendSignal("interrupt_action", self)

