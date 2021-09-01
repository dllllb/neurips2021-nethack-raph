from nethack_raph.Kernel import *
from nethack_raph.EeekObject import *
from nethack_raph.SignalReceiver import *

import random
import re


class Personality(EeekObject,SignalReceiver):
    def __init__(self):
        EeekObject.__init__(self)
        SignalReceiver.__init__(self)
        self.brains = []

    def nextAction(self):
        Kernel.instance.log("\n---- Personality ----)")
        self.curBrain.executeNext()

    def setBrain(self, brain):
        self.curBrain = brain
        Kernel.instance.log("Setting brain to %s" % str(brain))
