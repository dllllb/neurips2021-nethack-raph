import numpy as np

from nethack_raph.Brain import *
from nethack_raph.Pathing import dijkstra_pathing, mcp_pathing, check_neighbours

from nethack_raph.myconstants import DUNGEON_WIDTH


class TestBrain(Brain):
    def __init__(self, kernel):
        super().__init__("TestBrain", kernel)

        self.actions = {
            'Elbereth': Elbereth(kernel),
            'RestoreHP': RestoreHP(kernel),
            'EatFromInventory': EatFromInventory(kernel),
            'Pray': Pray(kernel),
            'RangeAttackMonster': RangeAttackMonster(kernel),
            'AttackMonster': AttackMonster(kernel),
            'Eat': Eat(kernel),
            'PickUpStuff': PickUpStuff(kernel),
            'FixStatus': FixStatus(kernel),
            'Explore': Explore(kernel),
            'OpenDoors': OpenDoors(kernel),
            # 'Descend': Descend(kernel),
            'Search': Search(kernel),
            # 'RandomWalk': RandomWalk(kernel),
        }
        self.prev_action = -1
        self.prev_path = []

    def execute_next(self, level):
        # first-fit action selection
        for name, action in self.actions.items():
            # check if an action can be taken
            can_act, mask = action.can(level)
            if not can_act:
                action.after_search(mask, None)
                continue

            # local actions do not need pathfinding and return mask = None
            if mask is None:
                action.execute()  # XXX path is None by default!
                action.after_search(None, None)
                break

            # actions that potentially require navigaton
            path = self.find_path(level, mask, name)
            action.after_search(mask, path)
            if path is None:
                self.kernel().log(f"Didn't find path for {name}")
                continue

            self.prev_action, self.prev_path = name, path
            self.kernel().log(f'found path length {len(path)} for {name}')
            action.execute(path)
            break

    def find_path(self, level, coords, action):
        hero = self.kernel().hero
        x, y = xy = hero.coords()  # hero.x, hero.y
        if coords[xy]:  # we are at the aim already
            return [xy]

        start = int(x * DUNGEON_WIDTH + y)
        flat_coords = coords.reshape(-1)

        use_prev_path = True
        if action != self.prev_action:  # doing not the same action as before
            use_prev_path = False
        elif len(self.prev_path) <= 3:  # less then 2 steps remaining
            use_prev_path = False
        elif self.prev_path[-2] != xy:  # didn't make a step to the right direction
            use_prev_path = False
        elif level.tiles.walk_cost[self.prev_path[-3]] != 1:  # Next step is not save
            use_prev_path = False
        elif check_neighbours(start, flat_coords):  # there is a goal nearby
            use_prev_path = False

        if use_prev_path:
            self.kernel().log(f'Use previous path')
            return self.prev_path[:-1]

        path, *ignore = dijkstra_pathing(level.tiles, xy, coords)

        return path
