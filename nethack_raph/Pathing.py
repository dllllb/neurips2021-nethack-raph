from nethack_raph.EeekObject import *
from nethack_raph.Tile import *

import heapq


class Node:
    def __init__(self, tile, cost):
        self.total_cost = cost
        self.tile = tile

    def __lt__(self, other):
        return self.total_cost < other.total_cost

    def __hash__(self):
        return self.tile.x + self.tile.y * WIDTH

    def __eq__(self, other):
        return self.tile.x == other.tile.x and self.tile.y == other.tile.y


def make_node(tile, cost):
    return Node(tile, cost)


class PriorityQueue:
    def __init__(self):
        self.elements = []

    def empty(self):
        return not self.elements

    def push(self, item):
        heapq.heappush(self.elements, item)

    def pop(self):
        return heapq.heappop(self.elements)


def reconstruct_path(came_from, start, goal):
    current = goal
    result = TileNode(goal.tile, 0)
    while current.tile != start.tile:
        current = came_from[current]
        result = TileNode(current.tile, result)
    return result


def dijkastra(start, condition_fns):
    start_node = make_node(start, 0)
    frontier = PriorityQueue()
    frontier.push(start_node)
    came_from = {start_node: None}
    cost_so_far = {start_node: 0}
    results = [None] * len(condition_fns)
    n_results = 0

    while not frontier.empty():
        current = frontier.pop()
        for condition_id, condition in enumerate(condition_fns):
            if results[condition_id] is None and condition(condition_id, current.tile):
                results[condition_id] = reconstruct_path(came_from, start_node, current)
                n_results += 1
            if n_results == len(results):
                return results

        for neighbour in current.tile.walkableNeighbours():
            neighbour_cost = cost_so_far[current] + Tile.walkables.get(neighbour.glyph, 1)
            neighbour_node = make_node(neighbour, neighbour_cost)
            if neighbour_node not in cost_so_far or neighbour_cost < cost_so_far[neighbour_node]:
                cost_so_far[neighbour_node] = neighbour_cost
                frontier.push(neighbour_node)
                came_from[neighbour_node] = current
    return results


class Pathing(EeekObject):
    def __init__(self):
        EeekObject.__init__(self)
        self.end = None

    def path(self, start=None, end=None, find=None, max_g=15):
        if not start:
            start = Kernel.instance.curTile()
        if end:
            self.end = end
            if not end.isWalkable():
                Kernel.instance.die("Asked for unwalkable square")
                return None
            elif end == start:
                Kernel.instance.die("end == start in Pathing.path()")
                return None
        else:
            self.end = None
            if not find:
                Kernel.instance.die("No end or find in path()\n  Start:%s\n  End:%s" % (str(start), str(end)))

        Kernel.instance.log("Finding path from\n    st:%s\n    en:%s\n    fi:%s" % (str(start), str(end), str(find)))

        open   = [self.createNode(start, 0)]
        closed = []

        while open:
            # Find the most promising square
            current = open[0]
            for x in open:
                if x.f() < current.f():
                    current = x

            if self.end:
                if current.tile == self.end:
                    return current

            if find:
                if current.tile.find(find):
                    return current

            if max_g and current.g >= max_g:
                return None
            # Switch it over to closed
            open.remove(current)
            closed.append(current)

            # For each of its walkable neighbours:
            for neighbour in current.tile.walkableNeighbours():
                # Ignore it if it's already in closed
                if [x for x in closed if x.tile == neighbour]:
                    continue

                neighbourNode = self.createNode(neighbour, current)
                if self.end:
                    if neighbourNode.tile == self.end:
                        return neighbourNode

                if find:
                    if neighbourNode.tile.find(find):
                        return neighbourNode

                openNode = None
                for n in open:
                    if n.tile == neighbour:
                        openNode = n
                        break

                # Add to open if it's not already in it
                if not openNode:
                    open.append(neighbourNode)
                else:
                    # If it is, and G is better: swaptime!
                    if openNode.g > neighbourNode.g:
                        open.remove(openNode)
                        open.append(neighbourNode)

        Kernel.instance.log("open is now empty. Did not find anything in Pathing")
        return None

    def createNode(self, tile, parent):
        tmp = TileNode(tile, parent)
        if parent and tile.glyph:
            if tile.glyph in Tile.walkables.keys():
                tmp.g = parent.g + Tile.walkables[tile.glyph]
            else:
                tmp.g = parent.g + 1
        else:
            tmp.g = 0


        if self.end:
            tmp.h = abs(tile.x-self.end.x) + abs(tile.y-self.end.y)
        else:
            tmp.h = 0
        return tmp

    def getDirection(self, tile):
        Kernel.instance.log(tile)
        if abs(Kernel.instance.curTile().y - tile.y) > 1 or abs(Kernel.instance.curTile().x - tile.x) > 1:
            Kernel.instance.die("Asked for directions to a nonadjacent tile: %s" % tile)
        if Kernel.instance.curTile().y <  tile.y and Kernel.instance.curTile().x <  tile.x: return 'n'
        if Kernel.instance.curTile().y <  tile.y and Kernel.instance.curTile().x == tile.x: return 'j'
        if Kernel.instance.curTile().y <  tile.y and Kernel.instance.curTile().x >  tile.x: return 'b'
        if Kernel.instance.curTile().y == tile.y and Kernel.instance.curTile().x <  tile.x: return 'l'
        if Kernel.instance.curTile().y == tile.y and Kernel.instance.curTile().x >  tile.x: return 'h'
        if Kernel.instance.curTile().y >  tile.y and Kernel.instance.curTile().x <  tile.x: return 'u'
        if Kernel.instance.curTile().y >  tile.y and Kernel.instance.curTile().x == tile.x: return 'k'
        if Kernel.instance.curTile().y >  tile.y and Kernel.instance.curTile().x >  tile.x: return 'y'


class TileNode:
    def __init__(self, tile, parent):
        self.tile   = tile
        self.parent = parent

        self.g = 0
        self.h = 0

    def f(self):
        return self.g + self.h

    def draw(self, color=41):
        a = self
        while a.parent != 0:
            Kernel.instance.stdout("\x1b[%dm\x1b[%d;%dH%s\x1b[m" % (color, a.tile.y+2, a.tile.x+1, a.tile.appearance()))
            a = a.parent

    def isWalkable(self):
        a = self
        while a.parent != 0:
            if not a.tile.isWalkable():
                return False
            a = a.parent
        return True

    def __getitem__(self, i):
        reverse = False
        if i < 0:
            i = abs(i)
            reverse = True
        if len(self) < i:
            raise IndexError

        if reverse:
            toReturn = len(self)-i
        else:
            toReturn = i

        count = 0
        a = self
        while a.parent != 0:
            if count == toReturn:
                break
            a = a.parent
            count = count + 1
        return a

    def __len__(self):
        count = 1
        a = self
        while a.parent != 0:
            a = a.parent
            count = count + 1
        return count

    def __str__(self):
        ret = str(self.tile.coords())
        a = self
        while a.parent != 0:
            a = a.parent
            ret = ret + ",(" + str(a.tile.coords()) +")"
        return ret
