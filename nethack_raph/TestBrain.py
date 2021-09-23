from nethack_raph.Brain import *
from nethack_raph.Pathing import dijkstra


class TestBrain(Brain):
    def __init__(self, kernel):
        Brain.__init__(self, "TestBrain", kernel)

        self.actions = [
                            Elbereth(kernel),
                            RestoreHP(kernel),
                            AttackMonster(kernel),
                            EatFromInventory(kernel),
                            Eat(kernel),
                            Pray(kernel),
                            # WearArmor(kernel),
                            FixStatus(kernel),
                            Explore(kernel),
                            OpenDoors(kernel),
                            # [DipForExcalibur(), 1600],
                            # [GetPhatz(),        1500],
                            Descend(kernel),
                            SearchSpot(kernel),
                            Search(kernel),
                            RandomWalk(kernel),
                       ]

    def executeNext(self):
        self.kernel().log(self.actions)
        condition_fns = []
        enabled_coords = []
        enabled_actions = []
        for action in self.actions:
            can_act, coords = action.can()
            if can_act:
                enabled_coords.append(coords)
                condition_fns.append(lambda coords_id, tile: enabled_coords[coords_id][tile.coords()])
                enabled_actions.append(action)

                path = dijkstra(self.kernel().curTile(), [lambda _, tile: coords[tile.coords()]])[0]
                action.after_search(path)

                if path is not None:
                    self.kernel().log(f'found path: {path} for {action}')
                    action.execute(path)
                    return
                else:
                    self.kernel().log(f"Didn't found path: for {action}")

    def s_isWeak(self):
        self.kernel().log("Praying because I'm weak")
        self.kernel().send("#pray\r")
