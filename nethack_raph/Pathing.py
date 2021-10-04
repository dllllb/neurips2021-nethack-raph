from nethack_raph.myconstants import DUNGEON_WIDTH, DUNGEON_HEIGHT

import heapq
import numpy as np

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
    def __init__(self, xy, cost):
        self.xy = xy
        self.total_cost = cost

    def __lt__(self, other):
        return self.total_cost < other.total_cost

    def __hash__(self):
        return self.xy

    def __eq__(self, other):
        return self.xy == other.xy


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
    result = [divmod(goal.xy, DUNGEON_WIDTH)]
    while current != start:
        current = came_from[current]
        result.append(divmod(current.xy, DUNGEON_WIDTH))
    return result


def dijkstra_pathing(walk_costs, start, condition_fns):
    start_node = Node(start, 0)
    frontier = PriorityQueue()
    frontier.push(start_node)
    came_from = {start_node: None}
    cost_so_far = {start_node: 0}
    results = [None] * len(condition_fns)
    n_results = 0

    while not frontier.empty():
        current = frontier.pop()
        for condition_id, condition in enumerate(condition_fns):
            if results[condition_id] is None and condition(condition_id, current.xy):
                results[condition_id] = reconstruct_path(came_from, start_node, current)
                n_results += 1
            if n_results == len(results):
                return results

        for neighbour in _NEIGHBOURS[current.xy]:
            walk_cost = walk_costs[neighbour]
            if not walk_cost: continue
            neighbour_cost = cost_so_far[current] + walk_cost
            neighbour_node = Node(neighbour, neighbour_cost)
            if neighbour_node not in cost_so_far or neighbour_cost < cost_so_far[neighbour_node]:
                cost_so_far[neighbour_node] = neighbour_cost
                frontier.push(neighbour_node)
                came_from[neighbour_node] = current
    return results


def check_neighbours(xy, coords):
    return bool(coords[np.array(_NEIGHBOURS[xy])].sum())


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
