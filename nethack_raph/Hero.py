from nethack_raph.TermColor import TermColor

import re


class Hero:
    def __init__(self, kernel):
        self.kernel = kernel
        self.x = None
        self.y = None
        self.beforeMove = None
        self.tmpCount = 0
        self.turns = 0

        self.attributes = None  # check https://nethackwiki.com/wiki/Attribute for more details

        self.score = 0
        self.curhp = None
        self.maxhp = None
        self.gold = None
        self.curpw = None

        self.maxpw = None
        self.armor_class = None
        self.xp = None
        self.xp_next = None

        self.blind = False
        self.confused = False
        self.hallu = False
        self.stun = False
        self.levitating = False
        self.legShape = True

        self.inBearTrap = False
        self.inPit = False
        self.isEngulfed = False
        self.isLycanthropy = False

        self.hunger = None
        self.god_is_angry = False

        self.role = None
        self.race = None
        self.gender = None
        self.moral = None

        self.lastActionedTile = None  # I sersiouly need to #enhance my english skills :'(
        self.lastAction = None
        self.lastActionedItem = None

        self.armor_class_before = None

    def coords(self):
        return self.y, self.x

    def update(self, blstats, top_line, bot_line):
        # TODO: use them
        # strength_percentage, monster_level, carrying_capacity, dungeon_number, level_number, condition
        # condition (aka `unk`) == 64 -> Deaf

        self.blind = bool(re.search("Blind", bot_line))
        self.confused = bool(re.search("Conf", bot_line))
        self.stun = bool(re.search("Stun", bot_line))
        self.hallu = bool(re.search("Hallu", bot_line))
        self.levitating = bool(re.search("Lev", bot_line))

        self.x, self.y, strength_percentage, strength, dexterity, constitution, \
            intelligence, wisdom, charisma, self.score, self.curhp, self.maxhp, \
            _, self.gold, self.curpw, self.maxpw, self.armor_class, monster_level, \
            self.xp, self.xp_next, self.turns, self.hunger, carrying_capacity, dungeon_number, \
            level_number, condition = blstats

        self.attributes = (strength, dexterity, constitution, intelligence, wisdom, charisma)
        self.kernel().log(f'Hero hp: {self.curhp}/{self.maxhp}')

    def attack(self, tile):
        dir = self._get_direction(self.kernel().curTile(), tile)
        self.kernel().drawString("Attacking -> %s (%s)" % (dir, tile))
        self.kernel().send("F"+dir)
        self.lastActionedTile = tile
        self.lastAction = 'attack'

    def move(self, tile):
        if self.beforeMove == (self.x, self.y) and self.tmpCount < 5 and not (self.inBearTrap or self.inPit):
            self.kernel().log("Hero asked to move, but I still havn't moved after last update, ignoring this")
            self.tmpCount = self.tmpCount + 1
        else:
            if self.beforeMove != (self.x, self.y):
                self.inBearTrap = False
                self.inPit = False
            else:
                if self.tmpCount > 3:
                    if not tile.char:
                        self.kernel().log("Made a door at %s" % tile)
                        tile.char = '-'
                        tile.color = TermColor(33, 0, False, False)
                        self.kernel().sendSignal("interrupt_action")

            dir = self._get_direction(self.kernel().curTile(), tile)
            self.kernel().drawString("Walking -> %s (%s)" % (dir, tile))

            self.beforeMove = (self.x, self.y)
            self.tmpCount = 0

            self.lastActionedTile = tile
            self.kernel().send(dir)
        self.lastAction = 'move'

    def descend(self):
        self.kernel().log("Hero is descending..")
        self.kernel().send(">")
        self.lastAction = 'descend'

    def open(self, tile):
        dir = self._get_direction(self.kernel().curTile(), tile)
        self.kernel().log("Hero is opening a door..")
        self.kernel().send("o%s" % dir)
        self.lastActionedTile = tile
        self.lastAction = 'open'

    def kick(self, tile):
        dir = self._get_direction(self.kernel().curTile(), tile)
        self.kernel().log("Hero is kicking a door..")
        self.kernel().send("\x04%s" % dir)
        self.lastAction = 'kick'

    def search(self, times=1):
        self.kernel().send("%ds" % times)
        for neighbour in self.kernel().curTile().neighbours():
            neighbour.searches = neighbour.searches + times
            if neighbour.searches >= self.kernel().curLevel().maxSearches:
                neighbour.searched = True
        self.lastAction = 'search'

    def eat(self):
        self.kernel().log("Hero::eat")
        self.kernel().send("e")
        self.lastAction = 'eat'

    def eat_from_inventory(self):
        self.kernel().log("Hero::eat from inventory")
        self.kernel().send("e")
        self.lastAction = 'eat_from_inventory'

    def read(self):
        self.kernel().log("Hero::read")
        self.kernel().send(":")
        self.kernel().curTile().has_elbereth = False
        self.lastAction = 'read'

    def write(self):
        self.kernel().log("Hero::write in the dust")
        self.kernel().send('E-')
        self.lastAction = 'write'

    def engrave(self):
        self.kernel().log("Hero::engrave")
        self.kernel().send('E')
        self.lastAction = 'engrave'

    def pray(self):
        self.kernel().log("Hero::pray")
        self.kernel().send('#pray\ry')
        self.lastAction = 'pray'

    def pick(self):
        self.kernel().log("Hero::pick")
        self.kernel().send(',')
        self.lastAction = 'pick'

    def wear(self, armor_letter):
        self.kernel().log("Hero::wear")
        self.kernel().send(f'W*{armor_letter}')
        self.armor_class_before = self.armor_class
        self.lastAction = 'wear'
        self.lastActionedItem = armor_letter

    def take_off(self, armor_letter):
        self.kernel().log("Hero::take_off")
        if self.kernel().inventory.being_worn_count > 1:
            # have to define, what we want to take off
            self.kernel().send(f'T*{armor_letter}')
        else:
            self.kernel().send('T')
        self.lastAction = 'take_off'
        self.kernel().hero.lastActionedItem = armor_letter

    def canPickupHeavy(self):
        # for poly and stuff
        return False

    def _get_direction(self, source, target):
        if abs(source.y - target.y) > 1 or abs(source.x - target.x) > 1:
            self.kernel().die(f"\n\nAsked for directions to a nonadjacent tile {source} -> {target}\n\n")
        if source.y < target.y and source.x < target.x:
            return 'n'
        if source.y < target.y and source.x == target.x:
            return 'j'
        if source.y < target.y and source.x > target.x:
            return 'b'
        if source.y == target.y and source.x < target.x:
            return 'l'
        if source.y == target.y and source.x > target.x:
            return 'h'
        if source.y > target.y and source.x < target.x:
            return 'u'
        if source.y > target.y and source.x == target.x:
            return 'k'
        if source.y > target.y and source.x > target.x:
            return 'y'

    def set_attributes(self, msg):
        if 'Archeologist' in msg:
            self.role = 'arc'
        elif 'Barbarian' in msg:
            self.role = 'bar'
        elif 'Caveman' in msg or 'Cavewoman' in msg:
            self.role = 'cav'
        elif 'Healer' in msg:
            self.role = 'hea'
        elif 'Knight' in msg:
            self.role = 'kni'
        elif 'Monk' in msg:
            self.role = 'mon'
        elif 'Priest' in msg or 'Priestest' in msg:
            self.role = 'pri'
        elif 'Ranger' in msg:
            self.role = 'ran'
        elif 'Rogue' in msg:
            self.role = 'rogue'
        elif 'Samurai' in msg:
            self.role = 'sam'
        elif 'Tourist' in msg:
            self.role = 'tou'
        elif 'Valkyrie' in msg:
            self.role = 'val'
        elif 'Wizard' in msg:
            self.role = 'wiz'
        # else:
        #    raise Exception(f"Unknown role from '{msg}'")

        if 'human' in msg:
            self.race = 'hum'
        elif 'elf' in msg or 'elven' in msg:
            self.race = 'elf'
        elif 'dwar' in msg:
            self.race = 'dwa'
        elif 'gnom' in msg:
            self.race = 'gno'
        elif 'orc' in msg:
            self.race = 'orc'
        # else:
        #    raise Exception(f"Unknown race from '{msg}'")

        if 'female' in msg or 'woman' in msg or 'Priestess' in msg:
            self.gender = 'fem'
        elif 'male' in msg or 'man' in msg or 'Priest' in msg:
            self.gender = 'mal'
        # else:
        #    raise Exception(f"Unknown gender from '{msg}'")

        if 'neutral' in msg:
            self.moral = 'neu'
        elif 'lawful' in msg:
            self.moral = 'law'
        elif 'chaotic' in msg:
            self.moral = 'cha'
        # else:
        #    raise Exception(f"Unknown moral from '{msg}'")

        self.kernel().log(f"Hero is {self.role}-{self.race}-{self.moral}-{self.gender}")
