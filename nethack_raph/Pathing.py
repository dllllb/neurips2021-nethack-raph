from nethack_raph.myconstants import WIDTH
from nethack_raph.Tile import Tile

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
    result = [goal.tile]
    while current.tile != start.tile:
        current = came_from[current]
        result.append(current.tile)
    return result


def dijkstra(start, condition_fns):
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
            if results[condition_id] is None and condition(condition_id, current.tile):
                results[condition_id] = reconstruct_path(came_from, start_node, current)
                n_results += 1
            if n_results == len(results):
                return results

        for neighbour in current.tile.walkableNeighbours():
            neighbour_cost = cost_so_far[current] + Tile.walkables.get(neighbour.glyph, 1)
            neighbour_node = Node(neighbour, neighbour_cost)
            if neighbour_node not in cost_so_far or neighbour_cost < cost_so_far[neighbour_node]:
                cost_so_far[neighbour_node] = neighbour_cost
                frontier.push(neighbour_node)
                came_from[neighbour_node] = current
    return results
