import numpy as np
from math import isfinite

from heapq import heappop, heappush
from collections import defaultdict

from nethack_raph.myconstants import DUNGEON_WIDTH, DUNGEON_HEIGHT

# from skimage.graph import MCP


def calc_neighbours():
    offsets = {(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)}
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

_NEIGHBOURS = calc_neighbours()


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


def dijkstra_pathing(tiles, start, mask):
    walk_costs = tiles.walk_cost.reshape(-1)
    coords = mask.reshape(-1)
    start = int(start[0] * DUNGEON_WIDTH + start[1])

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

        for neighbour in _NEIGHBOURS[current.xy]:
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
    return coords[np.array(_NEIGHBOURS[xy])].any()


def mcp_pathing(walk_costs, start, coords):
    if coords[start]:
        return [start]

    end_points = [(i, j) for i, j in zip(*np.where(coords))]
    mcp = MCP(walk_costs, fully_connected=True)
    costs, traceback = mcp.find_costs([start], end_points, find_all_ends=False)
    costs_to_endpoints = costs[np.array([y for y, x in end_points]), np.array([x for y, x in end_points])]

    if costs_to_endpoints.min() == np.inf:
        return None

    else:
        closest_end_point = end_points[costs_to_endpoints.argmin()]
        path = mcp.traceback(closest_end_point)[::-1]
        return path
