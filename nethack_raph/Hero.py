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
        return self.x, self.y

    def update(self, blstats, top_line, bot_line):
        # TODO: use them
        # strength_percentage, monster_level, carrying_capacity, dungeon_number, level_number, condition
        # condition (aka `unk`) == 64 -> Deaf

        self.blind = bool(re.search("Blind", bot_line))
        self.confused = bool(re.search("Conf", bot_line))
        self.stun = bool(re.search("Stun", bot_line))
        self.hallu = bool(re.search("Hallu", bot_line))
        self.levitating = bool(re.search("Lev", bot_line))

        self.y, self.x, strength_percentage, strength, dexterity, constitution, \
            intelligence, wisdom, charisma, self.score, self.curhp, self.maxhp, \
            _, self.gold, self.curpw, self.maxpw, self.armor_class, monster_level, \
            self.xp, self.xp_next, self.turns, self.hunger, carrying_capacity, dungeon_number, \
            level_number, condition = blstats

        self.attributes = (strength, dexterity, constitution, intelligence, wisdom, charisma)
        self.kernel().log(f'Hero hp: {self.curhp}/{self.maxhp}, hero coords: {self.coords()}')

    def attack(self, tile):
        dir = self._get_direction(self.coords(), tile)
        self.kernel().drawString("Attacking -> %s (%s)" % (dir, tile))
        self.kernel().send("F"+dir)
        self.lastActionedTile = tile
        self.lastAction = 'attack'

    def move(self, tile):
        dir = self._get_direction(self.coords(), tile, allowed_door_diagonally=False)
        self.kernel().drawString("Walking -> %s (%s)" % (dir, tile))

        self.beforeMove = (self.x, self.y)
        self.kernel().send(dir)
        self.lastActionedTile = tile
        self.lastAction = 'move'

    def descend(self):
        self.kernel().log("Hero is descending..")
        self.kernel().send(">")
        self.lastAction = 'descend'

    def open(self, tile):
        dir = self._get_direction(self.coords(), tile)
        self.kernel().log("Hero is opening a door..")
        self.kernel().send("o%s" % dir)
        self.lastActionedTile = tile
        self.lastAction = 'open'

    def kick(self, tile):
        dir = self._get_direction(self.coords(), tile)
        self.kernel().log("Hero is kicking a door..")
        self.kernel().send("\x04%s" % dir)
        self.lastAction = 'kick'

    def search(self, times=1):
        self.kernel().send("%ds" % times)

        neighbours = self.kernel().curLevel().neighbours[self.kernel().hero.coords()]
        neighbours.searches += times
        neighbours.searched[neighbours.searches >= self.kernel().curLevel().maxSearches] = True

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

    def _get_direction(self, source, target, allowed_door_diagonally=True):
        source_x, source_y = source
        target_x, target_y = target

        if abs(source_y - target_y) > 1 or abs(source_x - target_x) > 1:
            self.kernel().die(f"\n\nAsked for directions to a nonadjacent tile {source} -> {target}\n\n")

        if not allowed_door_diagonally:
            # A small hack. can't move diagonally into the doorway and out of the doorway
            target_tile = self.kernel().curLevel().tiles[target]
            source_tile = self.kernel().curLevel().tiles[source]
            if (source_tile.is_opened_door or target_tile.is_opened_door) and abs(source_y - target_y) + abs(source_x - target_x) > 1:

                if self.kernel().curLevel().tiles[target_x, source_y].walkable_tile:
                    self.kernel().log(f'walk to {(target_x, source_y)} instead of {target}')
                    target_y = source_y

                elif self.kernel().curLevel().tiles[source_x, target_y].walkable_tile:
                    self.kernel().log(f'walk to {(source_x, target_y)} instead of {target}')
                    target_x = source_x

                else:
                    target_tile.shop_entrance = True
                    self.kernel().curLevel().update_walk_cost(target_tile)
                    self.kernel().log(f'{target} should be a shop_entrance')
                    return ' '

        if source_x < target_x and source_y < target_y:
            return 'n'
        if source_x < target_x and source_y == target_y:
            return 'j'
        if source_x < target_x and source_y > target_y:
            return 'b'
        if source_x == target_x and source_y < target_y:
            return 'l'
        if source_x == target_x and source_y > target_y:
            return 'h'
        if source_x > target_x and source_y < target_y:
            return 'u'
        if source_x > target_x and source_y == target_y:
            return 'k'
        if source_x > target_x and source_y > target_y:
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
