from nethack_raph.myconstants import HEIGHT, WIDTH, COLOR_BG_CYAN

import numpy as np


class OpenDoors:
    def __init__(self, kernel):
        self.kernel = kernel

    def can(self):
        goal_coords = np.zeros((HEIGHT, WIDTH))

        self.kernel().log("Looking for any doors on level..")

        find_door = False
        doors = self.kernel().curLevel().findDoors()
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
            assert path.tile == self.kernel().curTile()
            for tile in self.kernel().curTile().neighbours():
                if tile.is_door:
                    if tile.locked:
                        self.kernel().hero.kick(tile)
                    else:
                        self.kernel().hero.open(tile)
                    return
            self.kernel().log('door is absent')
            self.kernel().send(' ')
            return
        else:
            path.draw(color=COLOR_BG_CYAN)
            self.kernel().hero.move(path[1].tile)
            self.kernel().sendSignal("interrupt_action", self)

