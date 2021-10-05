import numpy as np

from nethack_raph.Actions.base import BaseAction
from nethack_raph.myconstants import COLOR_BG_YELLOW


class PickUpStuff(BaseAction):
    action_to_do = None

    def can(self, level):
        if self.kernel().inventory.take_off_armors:
            self.action_to_do = 'take_off'
            return True, np.ones(level.shape, dtype=bool)

        if self.kernel().inventory.new_armors:
            self.action_to_do = 'wear'
            return True, np.ones(level.shape, dtype=bool)

        if self.hero.levitating:  # You cannot reach the floor.
            return False, np.zeros(level.shape, dtype=bool)

        stuff_tiles = np.zeros(level.shape, dtype=bool)
        for xy, items in level.items.items():
            if level.tiles[xy].in_shop or level.tiles[xy].dropped_here:
                continue

            stuff = [it for it in items if it.item_type in ('armor', 'gold_piece')]
            if stuff:
                stuff_tiles[xy] = True
                self.action_to_do = 'pick_up'
                self.log(f"Found stuff {xy}: {list(map(str, stuff))}")

        return stuff_tiles.any(), stuff_tiles

    def execute(self, path):
        if self.action_to_do == 'wear':
            _, _, armor_letter = self.kernel().inventory.new_armors.pop(0)
            self.hero.wear(armor_letter)
            return

        if self.action_to_do == 'take_off':
            armor_letter = self.kernel().inventory.take_off_armors.pop(0)
            self.hero.take_off(armor_letter)
            return

        # fetch an item
        *tail, one = path
        hero = self.hero
        assert one == (hero.x, hero.y)

        # move closer
        if tail:
            self.draw_path(path, color=COLOR_BG_YELLOW)
            hero.move(tail[-1])
            return

        hero.pick()
