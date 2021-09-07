class Personality:
    def __init__(self, kernel):
        self.brains = []
        self.kernel = kernel

    def nextAction(self):
        self.kernel().log("\n---- Personality ----)")
        self.curBrain.executeNext()

    def setBrain(self, brain):
        self.curBrain = brain
        self.kernel().log("Setting brain to %s" % str(brain))
