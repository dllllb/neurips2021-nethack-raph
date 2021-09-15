from nethack_raph.myconstants import HEIGHT, WIDTH, COLOR_BG_YELLOW

import numpy as np


class Search:
    def __init__(self, kernel):
        self.kernel = kernel

    def can(self):
        target_tiles = np.zeros((HEIGHT, WIDTH))
        found = False

        self.kernel().log("Finding possible searchwalktos")

        for tile in filter(lambda t: not t.isWalkable() and not t.searched and t.char in {'|', '-', ' '}, self.kernel().curLevel().tiles):
            # TODO should preoritize them by count = len([x for x in neighbour.adjacent({'searched': False})])
            neighbours = list(filter(lambda t: t.explored and t.walkable and t.monster is None, tile.neighbours()))
            if len(neighbours):
                walkto = max(neighbours, key=lambda t: len([neigh for neigh in t.neighbours() if not neigh.searched]))
                target_tiles[walkto.coords()] = True
                found = True
        return found, target_tiles


    def can2(self):
        # FIXME (dima) check logick
        if self.recursion_depth > 5:
            self.recursion_depth = 0
            return False

        self.recursion_depth += 1

        if self.goal and self.goal.searched:
            self.kernel().log("Searched enough here. Let's move on")
            self.walkto = None
            self.goal = None

        if self.walkto and not self.walkto.isWalkable():
            self.walkto = None
            self.goal = None
            self.search = False

        if not self.walkto:
            self.kernel().log("Finding possible searchwalktos")
            searchwalktos = self.kernel().curLevel().find({'isWalkable': False, 'searched': False})
            if searchwalktos:
                best = None
                for tile in searchwalktos:
                    if tile.char not in ['|', '-', ' ']:
                        continue
                    neighbours = tile.adjacent({'explored': True, 'walkable': True, 'monster': None})
                    # neighbours = [neib for neib in neighbours if neib not in self._reset_walktos] # (dima)
                    if neighbours:
                        if (best and tile.tilesFromCurrent() < best[2]) or not best:
                            best = (tile, neighbours, neighbours[0].tilesFromCurrent())
                            continue

                if best:
                    self.kernel().log("Best searchspot: (%s)" % str(map(str, best)))
                    self.goal = best[0]
                    bestNeighbour = (best[1][0], 0)
                    for neighbour in best[1]:
                        count = len([x for x in neighbour.adjacent({'searched': False})])
                        if count > bestNeighbour[1]:
                            bestNeighbour = (neighbour, count)
                    self.walkto = bestNeighbour[0]

            if self.goal and self.goal.isAdjacent(self.kernel().curTile()) and self.goal.searches < self.kernel().curLevel().maxSearches:
                self.kernel().log("Searching tile (%s)" % str(self.walkto))
                self.search = True
                self.recursion_depth = 0
                return True


        if not self.walkto:
            self.recursion_depth = 0
            return False


        if self.walkto == self.kernel().curTile():
            self.kernel().log("Searching tile (%s)" % str(self.walkto))
            self.search = True
            self.recursion_depth = 0
            return True

        elif self.walkto:
            self.kernel().log("Making a path to our walkto." + str(self.walkto))
            self.path = self.kernel().pathing.path(end=self.walkto)
            if self.path:
                self.kernel().log("Found a path.")
                self.recursion_depth = 0
                return True
            else:
                self.kernel().log("Recursing Search.can()..")
                self.kernel().stdout("\x1b[%dm\x1b[%d;%dH%s\x1b[m" % (
                    COLOR_BG_YELLOW, self.walkto.y, self.walkto.x, self.walkto.appearance()
                ))

                # FIXME: (dima) hack to prevent infinite recursion. Should be undone
                # self._reset_walktos.append(self.walkto)

                self.walkto = None
                self.goal = None
                self.path = None
                return self.can()
        self.kernel().curLevel().maxSearches = self.kernel().curLevel().maxSearches + 5
        self.recursion_depth = 0
        return False

    def after_search(self, path):
        if path is None:
            self.kernel().curLevel().maxSearches = self.kernel().curLevel().maxSearches + 5

    def execute(self, path):
        if len(path) == 1:
            assert path[0] == self.kernel().curTile()
            self.kernel().hero.search()
            return

        self.kernel().log("Going towards searchspot")
        self.kernel().draw_path(path, color=COLOR_BG_YELLOW)
        self.kernel().hero.move(path[-2])
        # self.kernel().sendSignal('interrupt_action', self)
