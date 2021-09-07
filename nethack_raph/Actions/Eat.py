from nethack_raph.myconstants import HEIGHT, WIDTH

import numpy as np


class Eat:
    def __init__(self, kernel):
        self.kernel = kernel

    def can(self):
        food_tiles = np.zeros((HEIGHT, WIDTH))

        if self.kernel().hero.hunger == 0:
            return False, food_tiles

        self.kernel().log(f"Hero have food: {self.kernel().hero.have_food}")

        if self.kernel().hero.have_food:
            return True, np.ones((HEIGHT, WIDTH))

        # return False, food_tiles

        foods = self.kernel().curLevel().find_food()
        self.kernel().log(f"Found {len(foods)} food tiles")
        found_food = False
        for food in foods:
            food_tiles[food.coords()] = True
            found_food = True
            self.kernel().log(f"Found {food}: {list(map(lambda t: str(t), food.items))}")
        return found_food, food_tiles

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

