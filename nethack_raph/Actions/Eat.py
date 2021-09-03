import nethack_raph.Kernel

from nethack_raph.Kernel import *
from nethack_raph.Pathing import TileNode
from nethack_raph.SignalReceiver import SignalReceiver


class Eat():
    def __init__(self):
        self.in_position = False
        self.path = None
        self.adj = None

    def can(self):
        self.in_position = False
        self.path = None
        self.adj = None

        if Kernel.instance.Hero.hanger == 0:
            return False

        # if Kernel.instance.Hero.hanger not in ['Hungry', 'Weak', 'Fainting']:
        #     return False

        # if Kernel.instance.Hero.have_food:
        #     return True

        Kernel.instance.log("Checking for adjacent food.." + str(Kernel.instance.Hero.hanger))

        if Kernel.instance.Hero.can_eat(Kernel.instance.curTile()):
            self.in_position = True
            Kernel.instance.log('curr is food')
            return True

        Kernel.instance.log("Looking for any foods on level..")

        foods = Kernel.instance.curLevel().find_food()
        for food in foods:
            #TODO check if we need walkable / explored here
            #for adjacent in food.walkableNeighbours():
            #    if not adjacent.explored:
            #        continue
            tmp = Kernel.instance.Pathing.a_star_search(end=food, max_g=self.path and self.path.g or None)
            if tmp and (self.path is None or self.path.g > tmp.g):
                self.path = tmp
        return self.path is not None

    def execute(self):
        if self.in_position:
            Kernel.instance.Hero.eat()
            # Kernel.instance.sendSignal("interrupt_action", self)
        else:
            Kernel.instance.log(self.path)
            Kernel.instance.Hero.move(self.path[1].tile)
            # Kernel.instance.sendSignal("interrupt_action", self)

