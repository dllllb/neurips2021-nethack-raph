from nethack_raph.Kernel import *
from nethack_raph.Pathing import TileNode


class Eat:
    def __init__(self):
        pass

    def can(self):
        food_tiles = np.zeros((HEIGHT, WIDTH))

        if Kernel.instance.Hero.hunger == 0:
            return False, food_tiles

        Kernel.instance.log(f"Hero have food: {Kernel.instance.Hero.have_food}")

        if Kernel.instance.Hero.have_food:
            return True, np.ones((HEIGHT, WIDTH))

        # return False, food_tiles

        foods = Kernel.instance.curLevel().find_food()
        Kernel.instance.log(f"Found {len(foods)} food tiles")
        found_food = False
        for food in foods:
            food_tiles[food.coords()] = True
            found_food = True
            Kernel.instance.log(f"Found {food}: {list(map(lambda t: str(t), food.items))}")
        return found_food, food_tiles

    def after_search(self, path):
        pass

    def execute(self, path):
        if len(path) == 1:
            assert path.tile == Kernel.instance.curTile()
            Kernel.instance.Hero.eat()
            return

        Kernel.instance.log(path)
        Kernel.instance.Hero.move(path[1].tile)
        # Kernel.instance.sendSignal("interrupt_action", self)

