from nethack_raph.myconstants import DUNGEON_HEIGHT, DUNGEON_WIDTH

import numpy as np


class EatFromInventory:
    def __init__(self, kernel):
        self.kernel = kernel

    def can(self):
        if self.kernel().hero.hunger == 0:
            self.kernel().log(f"Hero is Satiated")
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

    def can(self):
        if self.kernel().hero.hunger == 0:
            return False, np.zeros((DUNGEON_HEIGHT, DUNGEON_WIDTH))

        foods = self.kernel().curLevel().find_food()
        self.kernel().log(f"Found {len(foods)} food tiles")
        if foods:
            food_tiles = np.zeros((DUNGEON_HEIGHT, DUNGEON_WIDTH))
            for food in foods:
                food_tiles[food.coords()] = True
                self.kernel().log(f"Found {food}: {list(map(lambda t: str(t), food.items))}")
            return True, food_tiles

        return False, np.zeros((DUNGEON_HEIGHT, DUNGEON_WIDTH))

    def after_search(self, path):
        pass

    def execute(self, path):
        if len(path) == 1:
            assert path[0] == self.kernel().curTile()
            self.kernel().hero.eat()
            return

        self.kernel().log(path)
        self.kernel().hero.move(path[-2])
        # self.kernel().sendSignal("interrupt_action", self)

