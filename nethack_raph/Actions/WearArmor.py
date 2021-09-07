from nethack_raph.myconstants import HEIGHT, WIDTH

import numpy as np


class WearArmor:
    def __init__(self, kernel):
        self.kernel = kernel

    def can(self):
        armor_tiles = np.zeros((HEIGHT, WIDTH))
        found_armor = False
        for armor in filter(lambda t: sum([item.glyph == '[' and item.name != 'absent' for item in t.items]), self.kernel().curLevel().tiles):
            armor_tiles[armor.coords()] = True
            found_armor = True
            self.kernel().log(f"Found {armor}: {list(map(lambda t: str(t), armor.items))}")
        return found_armor, armor_tiles

    def after_search(self, path):
        pass

    def execute(self, path):
        if len(path) == 1:
            assert path[0] == self.kernel().curTile()
            self.kernel().send('W')
            self.kernel().log('HERO:WEAR')
            return

        self.kernel().log(path)
        self.kernel().hero.move(path[-2])
        # self.kernel().sendSignal("interrupt_action", self)

