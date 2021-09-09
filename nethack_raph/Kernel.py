from nethack_raph.myconstants import *
from nethack_raph.TermColor import TermColor
from nethack_raph.Personality import Personality
from nethack_raph.Senses import Senses
from nethack_raph.Console import Console
from nethack_raph.Hero import Hero
from nethack_raph.Dungeon import Dungeon
from nethack_raph.TestBrain import TestBrain
from nethack_raph.Cursor import Cursor

import re
import sys
import numpy as np
import weakref


class Kernel:
    def __init__(self, verbose):
        self._file = None
        self._frames_log = None
        self.verbose = False
        self.set_verbose(verbose)

        # Stuff
        # self.console = Console(weakref.ref(self))
        # self.cursor = Cursor(weakref.ref(self))
        self.dungeon = Dungeon(weakref.ref(self))
        self.hero = Hero(weakref.ref(self))

        # AI
        self.personality = Personality(weakref.ref(self))
        self.senses = Senses(weakref.ref(self))

        # Brains
        self.curBrain = TestBrain(weakref.ref(self))

        self.personality.setBrain(self.curBrain)  # Default brain

        self.signalReceivers = []

        self.action = ' '

        self.stdout("\u001b[2J\u001b[0;0H")
        self.state = None
        self.bot = None
        self.top = None
        self.inv_strs = None
        self.inv_letters = None

    def set_verbose(self, value):
        if not self.verbose and value:
            self._file = open("logs/log.txt", "w")
            self._frames_log = open("logs/frames.txt", "w")
        self.verbose = value

    def curLevel(self):
        return self.dungeon.curBranch.curLevel

    def curTile(self):
        return self.dungeon.curBranch.curLevel.tiles[self.hero.x + self.hero.y*WIDTH]

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

    def get_inventory_letter(self, inv_name):
        for letter, s in zip(self.inv_letters, self.inv_strs):
            descr = "".join([chr(ch) for ch in s])
            letter = chr(letter)
            if inv_name in descr:
                self.log(f'FOUND {inv_name}: {letter}, {descr}')
                return letter
        return ' '

    def step(self, obs):
        self.state = np.zeros((2, HEIGHT, WIDTH), dtype=np.uint8)
        self.state[0] = obs['tty_chars']
        self.state[1] = obs['tty_colors']
        self.bot = "".join(chr(ch) for ch in self.state[0].reshape(-1)[22*WIDTH:])
        self.top = "".join(chr(ch) for ch in self.state[0].reshape(-1)[:WIDTH])
        self.inv_strs = obs['inv_strs']
        self.inv_letters = obs['inv_letters']

        if len(self.action) != 0:
            self.action = self.action[1:]

        # self.frame_buffer.parse(obs)
        if self.verbose:
            TTY_BRIGHT = 8
            for y in range(0, HEIGHT):
                for x in range(0, WIDTH):
                    ch = chr(self.state[0][y, x])
                    color = 30 + int(self.state[1][y, x] & ~TTY_BRIGHT)
                    self.stdout("\x1b[%dm\x1b[%d;%dH%s" % (color, y+1, x+1, ch))
            self.logScreen()

        # TODO: use them
        #strength_percentage, monster_level, carrying_capacity, dungeon_number, level_number, unk

        self.hero.x, self.hero.y, strength_percentage, \
            self.hero.str, self.hero.dex, self.hero.con, \
            self.hero.int, self.hero.wis, self.hero.cha, \
            self.hero.score, self.hero.curhp, self.hero.maxhp, \
            self.dungeon.dlvl, self.hero.gold, self.hero.curpw, \
            self.hero.maxpw, self.hero.ac, monster_level, \
            self.hero.xp, self.hero.xp_next, self.hero.turns, \
            self.hero.hunger, carrying_capacity, dungeon_number, \
            level_number, unk = obs['blstats']

        # unk == 64 -> Deaf

        if self.searchBot("Blind"):
            self.hero.blind = True
        else:
            self.hero.blind = False

        if self.searchBot("the Werejackal"):
            self.hero.isPolymorphed = True

        # FIXME --more-- in the middle
        #if '--More--' in "".join([chr(ch) for ch in self.state[0].reshape(-1) if ch not in (ord('\n'), ord('\r'))]):
        #    self.action += ' '
        #    return self.action

        self.log("Updates starting: \n\n")
        self.log("--------- DUNGEON ---------")

        self.dungeon.update()
        if len(self.action):
            return self.action

        self.log("--------- SENSES --------- ")
        self.senses.update()
        if len(self.action):
            return self.action

        self.log("-------- MESSAGES -------- ")
        self.senses.parse_messages()
        if len(self.action):
            return self.action

        self.log("------ PERSONALITY ------  ")
        self.personality.nextAction()

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
        if self.verbose:
            self._file.write("%s"%str+"\n")
            self._file.flush()

    def die(self, msg):
        if self.verbose:
            self.stdout("\x1b[35m\x1b[3;1H%s\x1b[m\x1b[25;0f" % msg)
            self.log(msg)
        self.action = '#quit\ry'

    def drawString(self, msg):
        if self.verbose:
            self.log("Currently -> "+msg)
            self.stdout("\x1b[35m\x1b[25;0H%s\x1b[m" % msg + " "*(240-len(msg)))

    def addch(self, y, x, char, c=None):
        if self.verbose:
            self.stdout("%s\x1b[%d;%dH%s\x1b[m" % (c and "\x1b[%dm" % c or "", y, x, char))

    def draw_path(self, path, color=41):
        if self.verbose:
            for tile in path:
                self.stdout("\x1b[%dm\x1b[%d;%dH%s\x1b[m" % (color, tile.y + 2, tile.x + 1, tile.appearance()))

    def dontUpdate(self):
        pass
        # self.Dungeon.dontUpdate()
        # self.Personality.dontUpdate()
        # self.Senses.dontUpdate()

    def logScreen(self):
        if not self.verbose:
            return

        for y in range(0, HEIGHT):
            self._frames_log.write("\n")
            for x in range(0, WIDTH):
                if y == HEIGHT-1 and x > WIDTH-5:
                    break
                self._frames_log.write(chr(self.state[0][y,x]))
        if self.dungeon.curBranch:
            self._frames_log.write(str(self.curTile().coords()))
        self._frames_log.flush()

    def stdout(self, msg):
        if self.verbose:
            sys.stdout.write(msg)
            sys.stdout.flush()

