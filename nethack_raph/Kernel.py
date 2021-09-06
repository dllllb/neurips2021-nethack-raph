from nethack_raph.myconstants import *
from nethack_raph.TermColor import TermColor

import re
import sys
import numpy as np


class Kernel:
    instance = None

    def __init__(self, silent):
        self.silent = silent

        self.signalReceivers = []

        if not self.silent:
            self._file = open("logs/log.txt", "w")
            self._frames_log = open("logs/frames.txt", "w")

        Kernel.instance = self

        self.action = ' '

        self.stdout("\u001b[2J\u001b[0;0H")
        self.state = None
        self.bot = None
        self.top = None

    def curLevel(self):
        return self.Dungeon.curBranch.curLevel

    def curTile(self):
        return self.Dungeon.curBranch.curLevel.tiles[Kernel.instance.Hero.x + Kernel.instance.Hero.y*WIDTH]

    def searchBot(self, regex):
        return re.search(regex, self.bot)

    def searchTop(self, regex):
        return re.search(regex, self.top)

    def top_line(self):
        return self.top

    def bot_line(self):
        return self.bot

    def get_row_line(self, row):
        if row < 1 or row > 24:
            return ""
        return "".join(chr(ch) for ch in self.state[0].reshape(-1)[(row-1)*WIDTH:row*WIDTH])

    def step(self, obs):
        self.state = np.zeros((2, HEIGHT, WIDTH), dtype=np.uint8)
        self.state[0] = obs['tty_chars']
        self.state[1] = obs['tty_colors']
        self.bot = "".join(chr(ch) for ch in self.state[0].reshape(-1)[22*WIDTH:])
        self.top = "".join(chr(ch) for ch in self.state[0].reshape(-1)[:WIDTH])

        if len(self.action) != 0:
            self.action = self.action[1:]

        # self.frame_buffer.parse(obs)
        if not self.silent:
            TTY_BRIGHT = 8
            for y in range(0, HEIGHT):
                for x in range(0, WIDTH):
                    ch = chr(self.state[0][y, x])
                    color = 30 + int(self.state[1][y, x] & ~TTY_BRIGHT)
                    self.stdout("\x1b[%dm\x1b[%d;%dH%s" % (color, y+1, x+1, ch))
            self.logScreen()

        # TODO: use them
        #strength_percentage, monster_level, carrying_capacity, dungeon_number, level_number, unk

        Kernel.instance.Hero.x, Kernel.instance.Hero.y, strength_percentage, \
        Kernel.instance.Hero.str, Kernel.instance.Hero.dex, Kernel.instance.Hero.con, \
        Kernel.instance.Hero.int, Kernel.instance.Hero.wis, Kernel.instance.Hero.cha, \
        Kernel.instance.score, Kernel.instance.Hero.curhp, Kernel.instance.Hero.maxhp, \
        Kernel.instance.Dungeon.dlvl, Kernel.instance.Hero.gold, Kernel.instance.Hero.curpw, \
        Kernel.instance.Hero.maxpw, Kernel.instance.Hero.ac, monster_level, \
        Kernel.instance.Hero.xp, Kernel.instance.Hero.xp_next, Kernel.instance.turns, \
        Kernel.instance.Hero.hunger, carrying_capacity, dungeon_number, \
        level_number, unk = obs['blstats']

        # unk == 64 -> Deaf

        if Kernel.instance.searchBot("Blind"):
            Kernel.instance.Hero.blind = True
        else:
            Kernel.instance.Hero.blind = False

        if Kernel.instance.searchBot("the Werejackal"):
            Kernel.instance.Hero.isPolymorphed = True

        #FIXME --more-- in the middle
        #if '--More--' in self.frame_buffer.allLines():
        #    self.action += ' '
        #    return self.action

        self.log("Updates starting: \n\n")
        self.log("--------- DUNGEON ---------")

        self.Dungeon.update()
        if len(self.action):
            return self.action

        self.log("--------- SENSES --------- ")
        self.Senses.update()
        if len(self.action):
            return self.action

        self.log("-------- MESSAGES -------- ")
        self.Senses.parseMessages()
        if len(self.action):
            return self.action

        self.log("------ PERSONALITY ------  ")
        self.Personality.nextAction()

        self.log("\n\nUpdates ended.")
        return self.action

    def addSignalReceiver(self, sr):
        self.signalReceivers.append(sr)

    def sendSignal(self, s, *args, **args2):
        self.log("Sending signal " + s)
        for sr in self.signalReceivers:
            sr.signal(s, *args, **args2)

    def send(self, line):
        self.action = self.action + line

    def log(self, str):
        if not self.silent:
            self._file.write("%s"%str+"\n")
            self._file.flush()

    def die(self, msg):
        if not self.silent:
            self.stdout("\x1b[35m\x1b[3;1H%s\x1b[m\x1b[25;0f" % msg)
            self.log(msg)
        self.action = '#quit\ry'

    def drawString(self, msg):
        Kernel.instance.log("Currently -> "+msg)
        self.stdout("\x1b[35m\x1b[25;0H%s\x1b[m" % msg + " "*(240-len(msg)))

    def addch(self, y, x, char, c=None):
        self.stdout("%s\x1b[%d;%dH%s\x1b[m" % (c and "\x1b[%dm" % c or "", y, x, char))

    def dontUpdate(self):
        pass
        # self.Dungeon.dontUpdate()
        # self.Personality.dontUpdate()
        # self.Senses.dontUpdate()

    def logScreen(self):
        if self.silent:
            return

        for y in range(0, HEIGHT):
            self._frames_log.write("\n")
            for x in range(0, WIDTH):
                if y == HEIGHT-1 and x > WIDTH-5:
                    break
                self._frames_log.write(chr(self.state[0][y,x]))
        if Kernel.instance.Dungeon.curBranch:
            self._frames_log.write(str(Kernel.instance.curTile().coords()))
        self._frames_log.flush()

    def stdout(self, msg):
        if not self.silent:
            sys.stdout.write(msg)
            sys.stdout.flush()

