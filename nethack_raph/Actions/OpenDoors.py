from nethack_raph.Kernel import *
import numpy as np


class OpenDoors:
    def __init__(self):
        pass

    def can(self):
        goal_coords = np.zeros((HEIGHT, WIDTH))

        Kernel.instance.log("Looking for any doors on level..")

        find_door = False
        doors = Kernel.instance.curLevel().findDoors()
        for door in doors:
            for adjacent in door.walkableNeighbours():
                if not adjacent.explored:
                    continue
                goal_coords[adjacent.coords()] = True
                find_door = True

        return find_door, goal_coords

    def after_search(self, path):
        pass

    def execute(self, path):
        if len(path) == 1:
            assert path.tile == Kernel.instance.curTile()
            for tile in Kernel.instance.curTile().neighbours():
                if tile.is_door:
                    if tile.locked:
                        Kernel.instance.Hero.kick(tile)
                    else:
                        Kernel.instance.Hero.open(tile)
                    return
            Kernel.instance.log('door is absent')
            Kernel.instance.send(' ')
            return
        else:
            path.draw(color=COLOR_BG_CYAN)
            Kernel.instance.Hero.move(path[1].tile)
            Kernel.instance.sendSignal("interrupt_action", self)

