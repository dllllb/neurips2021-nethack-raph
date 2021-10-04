from nethack_raph.myconstants import DUNGEON_HEIGHT, DUNGEON_WIDTH

import numpy as np


class PickUpStuff:
    def __init__(self, kernel):
        self.kernel = kernel
        self.action_to_do = None

    def can(self, level):
        if self.kernel().inventory.take_off_armors:
            self.action_to_do = 'take_off'
            return True, np.ones((DUNGEON_HEIGHT, DUNGEON_WIDTH))

        if self.kernel().inventory.new_armors:
            self.action_to_do = 'wear'
            return True, np.ones((DUNGEON_HEIGHT, DUNGEON_WIDTH))

        if self.kernel().hero.levitating:  # You cannot reach the floor.
            return False, np.zeros((DUNGEON_HEIGHT, DUNGEON_WIDTH))

        stuff_tiles = np.zeros((DUNGEON_HEIGHT, DUNGEON_WIDTH))
        for xy, items in level.items.items():
            if level.tiles[xy].in_shop or level.tiles[xy].dropped_here: continue
            if any([item.item_type in ('armor', 'gold_piece') for item in items]):
                stuff_tiles[xy] = True
                self.action_to_do = 'pick_up'
                self.kernel().log(f"Found stuff {xy}: {list(map(lambda t: str(t), items))}")

        return stuff_tiles.sum() > 0, stuff_tiles

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
            assert path[0] == tuple(self.kernel().curTile().xy)
            self.kernel().hero.pick()
            return

        self.kernel().log(path)
        self.kernel().hero.move(path[-2])
