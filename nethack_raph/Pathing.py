import numpy as np
from math import isfinite

from heapq import heappop, heappush
from collections import defaultdict

from nethack_raph.myconstants import DUNGEON_WIDTH, DUNGEON_HEIGHT


def calc_corner_adjacent():
    offsets = {(-1, -1), (-1, 1), (1, -1), (1, 1)}
    result = []
    for x in range(DUNGEON_HEIGHT):
        for y in range(DUNGEON_WIDTH):
            neibs = []
            for h, w in offsets:
                if x + h >= DUNGEON_HEIGHT: continue
                if x + h < 0: continue
                if y + w >= DUNGEON_WIDTH: continue
                if y + w < 0: continue
                neibs.append((x + h) * DUNGEON_WIDTH + y + w)
            result.append(tuple(neibs))
    return result


def calc_edge_adjacent():
    offsets = {(-1, 0), (0, -1), (0, 1), (1, 0)}
    result = []
    for x in range(DUNGEON_HEIGHT):
        for y in range(DUNGEON_WIDTH):
            neibs = []
            for h, w in offsets:
                if x + h >= DUNGEON_HEIGHT: continue
                if x + h < 0: continue
                if y + w >= DUNGEON_WIDTH: continue
                if y + w < 0: continue
                neibs.append((x + h) * DUNGEON_WIDTH + y + w)
            result.append(tuple(neibs))
    return result

_CORNER_ADJACENT = calc_corner_adjacent()
_EDGE_ADJACENT = calc_edge_adjacent()


class Node:
    __slots__ = 'xy', 'cost'

    def __init__(self, xy, cost):
        self.xy = xy
        self.cost = cost

    def __lt__(self, other):
        return self.cost < other.cost

    def __hash__(self):
        return self.xy

    def __eq__(self, other):
        return self.xy == other.xy


def reconstruct_path(prev, goal):
    result = []
    while goal is not None:
        result.append(divmod(goal.xy, DUNGEON_WIDTH))
        goal = prev[goal]
    return result


def dijkstra_pathing(tiles, start, mask, doors):
    walk_costs = tiles.walk_cost.reshape(-1)
    coords = mask.reshape(-1)
    doors = doors.reshape(-1)
    start = int(start[0] * DUNGEON_WIDTH + start[1])

    def neighbours_gen(xy, doors):
        for neib in _EDGE_ADJACENT[xy]:
            yield neib
        if not doors[xy]:
            for neib in _CORNER_ADJACENT[xy]:
                if not doors[neib]:
                    yield neib

    cost = defaultdict(lambda: float('inf'))
    prev = {}

    # init start
    node = Node(start, 0)
    frontier = [node]
    cost[node] = 0.
    prev[node] = None

    # run dijkstra with premature termination
    while frontier:
        current = heappop(frontier)

        if coords[current.xy]:
            return reconstruct_path(prev, current),

        # no need to re-inspect stale heap records
        if cost[current] < current.cost:
            continue

        # edge adjacent
        for neighbour in neighbours_gen(current.xy, doors):
            # consider tiles with finite +ve costs only
            walk_cost = walk_costs[neighbour]
            if isfinite(walk_cost) and walk_cost >= 0:

                node = Node(neighbour, cost[current] + walk_cost)
                if node.cost < cost[node]:
                    heappush(frontier, node)

                    cost[node] = node.cost
                    prev[node] = current

    return None,


def check_neighbours(xy, coords):
    return coords[np.array(_EDGE_ADJACENT[xy])].any() or coords[np.array(_CORNER_ADJACENT[xy])].any()
