from nethack_raph.Kernel import *


class WearArmor:
    def __init__(self):
        pass

    def can(self):
        armor_tiles = np.zeros((HEIGHT, WIDTH))
        found_armor = False
        for armor in filter(lambda t: sum([item.glyph == '[' and item.name != 'absent' for item in t.items]), Kernel.instance.curLevel().tiles):
            armor_tiles[armor.coords()] = True
            found_armor = True
            Kernel.instance.log(f"Found {armor}: {list(map(lambda t: str(t), armor.items))}")
        return found_armor, armor_tiles

    def after_search(self, path):
        pass

    def execute(self, path):
        if len(path) == 1:
            assert path.tile == Kernel.instance.curTile()
            Kernel.instance.send('W')
            Kernel.instance.log('HERO:WEAR')
            return

        Kernel.instance.log(path)
        Kernel.instance.Hero.move(path[1].tile)
        # Kernel.instance.sendSignal("interrupt_action", self)

