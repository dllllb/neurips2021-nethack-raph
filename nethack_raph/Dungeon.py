from nethack_raph.Kernel import *
from nethack_raph.EeekObject import *
from nethack_raph.Branch import *


class Dungeon(EeekObject):
    def __init__(self):
        EeekObject.__init__(self)

        self.branches = [Branch("Main"), Branch("Mines"), Branch("Sokoban"), Branch("Quest"), Branch("Gehennom"), Branch("Planes"), Branch("Unknown")]
        self.curBranch = None
        self.dlvl = -1

    def tile(self, y, x):
        return self.curBranch.curLevel.tiles[x + y*WIDTH]

    def update(self):
        if not self.curBranch or self.curBranch.curLevel.dlvl != self.dlvl:
            self.curBranch = self.guessBranch()
            Kernel.instance.sendSignal("new_dlvl")

        self.curBranch.update()

    def guessBranch(self):
        if self.dlvl < 2 or (self.dlvl > WHEREIS_MINES[-1] and self.dlvl < WHEREIS_GEHENNOM[0]):
            return [branch for branch in self.branches if branch.name == "Main"][0]
        else:
            return [branch for branch in self.branches if branch.name == "Unknown"][0]
