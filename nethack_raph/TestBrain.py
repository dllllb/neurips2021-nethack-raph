from nethack_raph.Brain import *
from nethack_raph.Pathing import dijkastra


class TestBrain(Brain):
    def __init__(self):
        Brain.__init__(self, "TestBrain")

        self.actions = [
                            AttackMonster(),
                            #[Eat(), 3500],
                            FixStatus(),
                            RestoreHP(),
                            SearchSpot(),
                            OpenDoors(),
                            # [DipForExcalibur(), 1600],
                            #[GetPhatz(),        1500],
                            Explore(),
                            Descend(),
                            Search(),
                            RandomWalk(),
                       ]

    def executeNext(self):
        Kernel.instance.log(self.actions)
        condition_fns = []
        enabled_coords = []
        enabled_actions = []
        for action in self.actions:
            can_act, coords = action.can()
            if can_act:
                enabled_coords.append(coords)
                condition_fns.append(lambda coords_id, tile: enabled_coords[coords_id][tile.coords()])
                enabled_actions.append(action)

                path = dijkastra(Kernel.instance.curTile(), [lambda _, tile: coords[tile.coords()]])[0]
                action.after_search(path)

                if path is not None:
                    Kernel.instance.log(f'found path: {path} for {action}')
                    action.execute(path)
                    return

    def s_isWeak(self):
        Kernel.instance.log("Praying because I'm weak")
        Kernel.instance.send("#pray\r")
