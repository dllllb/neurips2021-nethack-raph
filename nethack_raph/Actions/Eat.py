from nethack_raph.myconstants import DUNGEON_HEIGHT, DUNGEON_WIDTH

import numpy as np


class EatFromInventory:
    def __init__(self, kernel):
        self.kernel = kernel

    def can(self, state):
        if self.kernel().hero.hunger < 3:
            self.kernel().log(f"Hero is not weak")
            return False, np.zeros((DUNGEON_HEIGHT, DUNGEON_WIDTH))

        self.kernel().log(f"Hero have food: {self.kernel().inventory.have_food()}")

        if self.kernel().inventory.have_food():
            return True, np.ones((DUNGEON_HEIGHT, DUNGEON_WIDTH))
        else:
            return False, np.zeros((DUNGEON_HEIGHT, DUNGEON_WIDTH))

    def after_search(self, path):
        pass

    def execute(self, path):
        self.kernel().hero.eat_from_inventory()


class Eat:
    def __init__(self, kernel):
        self.kernel = kernel

    def can(self, level):
        if self.kernel().hero.hunger == 0:
            return False, np.zeros((DUNGEON_HEIGHT, DUNGEON_WIDTH))

        food_tiles = np.zeros((DUNGEON_HEIGHT, DUNGEON_WIDTH))
        for xy, items in level.items.items():
            if level.tiles[xy].char == '^' or level.tiles[xy].in_shop: continue
            if any([item.is_food and not item.is_tainted() for item in items]):
                food_tiles[xy] = True
                self.kernel().log(f"Found food {xy}: {list(map(lambda t: str(t), items))}")

        return food_tiles.sum() > 0, food_tiles

    def after_search(self, path):
        pass

    def execute(self, path):
        if len(path) == 1:
            assert path[0] == tuple(self.kernel().curTile().xy)
            self.kernel().hero.eat()
            return

        self.kernel().log(path)
        self.kernel().hero.move(path[-2])

