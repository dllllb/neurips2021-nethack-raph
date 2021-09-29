from nethack_raph.TermColor import TermColor
from nethack_raph.myconstants import TTY_HEIGHT, DUNGEON_WIDTH

import inspect
import re


class Senses:
    def __init__(self, kernel):
        self.kernel = kernel
        self.messages = []

        self.events = {
           #  "(needs food, badly!|feel weak now\.|feel weak\.)":              ['is_weak'],
            "You feel that .* is displeased.":                               ['is_displeased'],
            "There is a staircase (down|up) here":                           ['is_staircase_here'],
            "Your (right|left) leg is in no shape":                          ['leg_no_shape'],
            "Your leg feels somewhat better":                                ['leg_feels_better'],
            "You see here":                                                  ['found_items'],
            "Things that are here":                                          ['found_items'],
            "There are (several|many) objects here":                         ['found_items'],
            "There's some graffiti on the floor here":                       ['graffiti_on_floor'],
            "You read: \"(.*?)\"":                                           ['you_read'],
            "Velkommen, [^,]+!":                                             ['shop_entrance'],
            ".*elcome to .* (store|dealership|bookstore|emporium|outlet|delicatessen|jewelers|accessories|hardware|books|food|lighting).*":  ['shop_entrance'],
            "There is an open door here":                                    ['open_door_here'],
            "There is a bear trap here|You are caught in a bear trap":       ['found_beartrap'],
            "You feel more confident in your ([^ ]+) ":                      ['skill_up'],
            "You feel quick":                                                ['gain_instrinct', 'fast'],
            "You are momentarily blinded by a flash of light":               ['blinded'],
            "You are still in a pit|You fall into a pit":                    ['fell_into_pit'],
            "You are caught in a bear trap|A bear trap closes on your foot": ['stepped_in_beartrap'],
            "Click! You trigger":                                            ['trigger_trap'],
            "There is a magic trap here":                                    ['found_trap', 'magic'],
            "There is a falling rock trap|A trap door in the ceiling opens": ['found_trap', 'rock'],
            "There is an arrow trap":                                        ['found_trap', 'arrow'],
            "A board beneath you squeaks loudly":                            ['found_trap', 'squeek'],
            "This door is locked":                                           ['locked_door'],
            "Closed for inventory":                                          ['shopkeep_door'],
            "You get expelled":                                              ['got_expelled'],
            "There is a teleportation trap here":                            ['found_trap', 'teleport'],
            # r".* eat it\? \[ynq\] \(n\)":              ['eat_it'],
            "You see no door there.": ['no_door'],
            "You finish eating .*": ['food_is_eaten'],
            "You harmlessly attack a statue.": ['is_statue'],
            "You cannot pass through the bars.": ['not_walkable'],
            "You are carrying too much to get through.": ['not_walkable'],
            "Hello stranger, who are you?": ['who_are_you'],
            "It's solid stone.": ['not_walkable'],
            "Will you please leave your (.*) outside\?": ['leave_pick'],
            "Call a scroll .*": ['scroll'],
            "You don't have anything to eat.": ['no_food'],
            "You don't have anything else to wear.": ['no_wear'],
            "You don't have anything else to put on.": ['no_wear'],
            "Call a scroll labeled .*": ['read_scroll'],
            "(.+) engulfs you": ['got_engulfed'],
            "Call (.+) potion": ['call_potion'],
            "Hello Agent, welcome to NetHack!": ['start_message'],
            "You kill .*": ["killed_monster"],
            "Continue eating\? .*": ['stop_eating'],
            "You see no objects here.": ['nothing_found'],
            "You can't write on the .*": ['cant_write'],
            "You are hit.*": ['you_was_hit'],
            "There is nothing here to pick up.": ['no_pickup'],
            "The stairs are solidly fixed to the floor.": ['no_pickup'],
            "You could drink the water...": ['no_pickup'],
            "You cannot wear .*": ['cant_wear'],
            "You are already wearing .*": ['cant_wear'],
            "[a-z] - ": ['picked_up'],
            "You finish your dressing maneuver.": ['dressed'],
            "You finish taking off your mail.": ['took_off'],
        }

    def update(self):
        # XXX this is where the top line is used, can we reuse the message?
        top = self.kernel().top_line()
        self.messages = self.messages + top.strip().split("  ")
        self.kernel().log(str(self.messages))

        if self.kernel().searchTop("Things that are here:"):
            self.kernel().log("Found some items. (Row 3)")
            self.kernel().send("    ")

        elif self.kernel().get_row_line(3).find("Things that are here:") >= 0:
            self.messages.append("Things that are here:")
            self.kernel().log("Found some items (row 3).")
            self.kernel().send("    ")

        if self.kernel().searchTop("Really attack"):
            self.kernel().log("Asked if I really want to attack.")
            self.kernel().send("y")

        #TODO MOVE THE ABOWE TO UPDATE

        if self.kernel().searchTop("In what direction?"):
            self.kernel().log("Getting rid if 'In what direction?' prompt")
            self.kernel().send("\x1b")

        match = self.kernel().searchTop(r"What do you want to eat\? \[(.*) or \?\*\]")
        if match:
            self.what_to_eat(match)
            return

        elif self.kernel().searchTop(r".* eat .*\? \[ynq\] \(n\)"):
            self.eat_it(self.kernel().top_line())
            return

        elif self.kernel().searchTop(r"What do you want to write in the dust here\?"):
            self.kernel().send('Elbereth\r')
            return

        elif self.kernel().searchTop(r"Do you want to add to the current engraving\? \[ynq\] \(y\)"):
            self.kernel().send('n')
            return

        elif self.kernel().searchTop("You have a little trouble .*"):
            self.kernel().send('y')
            return

        elif self.kernel().searchTop("\? \[(.*?)\]"):
            self.kernel().log("Found a prompt we can't handle: %s" % self.kernel().top_line())
            self.kernel().send(" ")

    def got_expelled(self):
        self.kernel().log("Got expelled. Phew!")
        self.kernel().hero.isEngulfed = False

    def got_engulfed(self, match):
        self.kernel().log("We just got engulfed. This will confuze me a whole lot :(")
        self.kernel().hero.isEngulfed = True

    def shopkeep_door(self):
        for tile in self.kernel().curTile().neighbours():
            if tile.is_closed_door:
                tile.shopkeepDoor = True
                tile.update_is_walkable()

    def locked_door(self):
        if self.kernel().hero.lastActionedTile and self.kernel().hero.lastActionedTile.is_closed_door:
            self.kernel().hero.lastActionedTile.locked = True

    def found_trap(self, type):
        self.kernel().log("I found a trap. Setting char to ^")
        self.kernel().curTile().set_as_trap()

    def fell_into_pit(self):
        self.kernel().log("I fell into a pit :(")
        self.kernel().hero.inPit = True
        self.kernel().curTile().set_as_trap()

    def found_beartrap(self):
        self.kernel().log("Found a beartrap. Setting tile to ^")
        self.kernel().curTile().set_as_trap()

    def stepped_in_beartrap(self):
        self.kernel().log("Just stepped into a beartrap :(")
        self.kernel().hero.inBearTrap = True
        self.kernel().curTile().set_as_trap()

    def trigger_trap(self):
        self.kernel().log("Triggered a trap, setting char to ^.. Not changing color yet")
        self.kernel().curTile().set_as_trap()

    def blinded(self):
        self.kernel().log("I got blinded.")
        self.kernel().hero.blind = True

    def gain_instrinct(self, type):
        pass

    def skill_up(self, match):
        if match.groups()[0] == 'weapon':
            self.kernel().log("Enhanced weaponskill!")
            pass

    def open_door_here(self):
        self.kernel().log("Setting tile to '-' with door colors")
        self.kernel().curTile().setTile('-', TermColor(33, 0, False, False), 2373)

    def call_potion(self, match):
        self.kernel().send("\x1b")

    def eat_it(self, msg):
        if self.kernel().hero.lastAction == 'eat_from_inventory':
            self.kernel().log('eating from inventory. eating aborted')
            self.kernel().send('n')
            return

        if not all([item.is_food for item in self.kernel().curTile().items if item.char == '%']):
            # otherwise we should check that food in msg correspond to edible food
            self.kernel().log('not edible: eating aborted')
            self.kernel().send('n')
            for item in self.kernel().curTile().items:
                if item.char == '%':
                    item.is_food = False

        elif 'corpse' in msg and not bool([item.is_food for item in self.kernel().curTile().items if item.corpse]):
            self.kernel().log('unknown / not edible corpse: eating aborted')
            self.kernel().send('n')
            for item in self.kernel().curTile().items:
                if item.char == '%':
                    item.is_food = False

        else:
            self.kernel().log('eating...')
            self.kernel().send('y')

    def stop_eating(self, msg):
        # probably ate something wrong
        self.kernel().log('not edible: eating aborted')
        self.kernel().send('n')
        for item in self.kernel().curTile().items:
            if item.char == '%':
                item.is_food = False

    def no_door(self):
        if self.kernel().hero.lastActionedTile:
            self.kernel().hero.lastActionedTile.is_closed_door = False

    def what_to_eat(self, matched):
        options = matched.groups()[0]
        self.kernel().log('eating...' + options)
        if 'f' in options:
            self.kernel().send('f')
        else:
            self.kernel().send(options[0])

    def is_displeased(self):
        self.kernel().hero.god_is_angry = True

    def is_staircase_here(self, match):
        self.kernel().log("Found staircase under some items..")

        if match.groups()[0] == 'down':
            self.kernel().curTile().char = '>'
            self.kernel().curTile().color = TermColor(37, 0, False, False)
        else:
            self.kernel().curTile().char = '<'
            self.kernel().curTile().color = TermColor(37, 0, False, False)

    def leg_no_shape(self):
        #TODO DONT WORK
        self.kernel().log("Leg is not in shape :'(")
        self.kernel().hero.legShape = False

    def leg_feels_better(self):
        self.kernel().log("Leg is fine again.")
        self.kernel().hero.legShape = True

    def found_items(self, tmp, msg):
        self.kernel().log("Found some item(s)..")
        self.kernel().sendSignal("foundItemOnFloor")

    def shop_entrance(self, match, msg):
        self.kernel().log("Found a shop.")

        if self.kernel().curTile().is_opened_door and self.kernel().hero.lastAction == 'move':
            prev_coords = (self.kernel().hero.beforeMove[1], self.kernel().hero.beforeMove[0])
            cur_coords = self.kernel().hero.coords()
            # entrance is opposite to the tile where we came from
            entrance_y, entrance_x = tuple((2*c - p) for c, p in list(zip(cur_coords, prev_coords)))
            entrance_tile = self.kernel().dungeon.tile(entrance_y, entrance_x)

            entrance_tile.shop_entrance = True
            entrance_tile.update_is_walkable()
            self.kernel().log(f'Shop entrance: {entrance_tile}')

        buf = [self.kernel().curTile()]
        while buf:
            for tile in buf.pop().neighbours():
                # This could break once a year or so (if a monster is standing in a non-shop square after you login?)
                if (tile.char == '.' or (tile.monster and not tile.monster.pet) or tile.items) and not tile.inShop:
                    buf.append(tile)

                    self.kernel().log("Setting %s to be inside a shop." % tile)
                    tile.inShop = True
                    tile.update_is_walkable()

    def food_is_eaten(self):
        pass
        # self.kernel().curTile().items = []

    def no_food(self):
        for item in self.kernel().curTile().items:
            if item.char == '%':
                item.is_food = False

    def no_wear(self):
        self.kernel().inventory.new_armors = []

    def read_scroll(self):
        self.kernel().send('r\r') # 'r\r' seems to work

    def is_statue(self):
        if self.kernel().hero.lastActionedTile and self.kernel().hero.lastActionedTile.monster:
            self.kernel().hero.lastActionedTile.monster.is_statue = True

    def not_walkable(self):
        if self.kernel().hero.lastActionedTile:
            self.kernel().hero.lastActionedTile.walkable_glyph = False
            self.kernel().hero.lastActionedTile.update_is_walkable()

    def leave_pick(self, match):
        pass

    def who_are_you(self):
        self.kernel().send('Croseus\r')

    def scroll(self):
        self.kernel().send('r')

    def carrying_too_mach(self):
        # FIXME (dima) drop smth
        if self.kernel().hero.lastActionedTile:
            self.kernel().hero.lastActionedTile.walkable_glyph = False
            self.kernel().hero.lastActionedTile.update_is_walkable()

    def graffiti_on_floor(self):
        self.kernel().log("Found grafitti!")

    def start_message(self):
        msg = ' '.join(self.messages[1:])
        self.kernel().hero.set_attributes(msg)
        self.kernel().log(str(self.messages))

    def killed_monster(self, msg):
        if not self.kernel().hero.lastActionedTile or not self.kernel().hero.lastActionedTile.items:
            return

        for item in self.kernel().hero.lastActionedTile.items:
            if item.corpse:  # FIXME (nikita) check glyph of killed monster
                item.turn_of_death = self.kernel().hero.turns

    def you_read(self, match):
        self.kernel().log(f'YOU READ {match.groups()[0]}')
        self.kernel().curTile().has_elbereth = match.groups()[0] == 'Elbereth'

    def nothing_found(self):
        self.kernel().curTile().items = []

    def cant_write(self):
        if self.kernel().curTile().char is None:
            self.kernel().curTile().char = '{'

    def you_was_hit(self):
        if self.kernel().curTile().has_elbereth:
            # you was hit, possible from distance, elbereth doesn't protect you
            for tile in self.kernel().curLevel().tiles:
                if tile.monster and not tile.monster.pet:
                    tile.monster.range_attack = False

    def no_pickup(self):
        self.kernel().curTile().items = []

    def picked_up(self):
        self.kernel().curTile().items = []

    def dressed(self):
        if self.kernel().hero.armor_class >= self.kernel().hero.armor_class_before:
            self.kernel().inventory.take_off_armors.append(self.kernel().hero.lastActionedItem)

    def took_off(self):
        # Drop unused item:
        self.kernel().log(f'Drop item {self.kernel().hero.lastActionedItem}')
        self.kernel().send(f'd{self.kernel().hero.lastActionedItem}')
        self.kernel().curTile().dropped_here = True

    def cant_wear(self):
        # Drop unused item:
        self.kernel().log(f'Drop item {self.kernel().hero.lastActionedItem}')
        self.kernel().send(f'd{self.kernel().hero.lastActionedItem}')
        self.kernel().curTile().dropped_here = True
        # TODO (nikita): we can try take off another item, if we are already wearing that type of armor

    def parse_messages(self):
        for msg in self.messages:
            for event in self.events:
                match = re.search(event, msg)
                if match:
                    self.kernel().log("Found message: %s" % event)
                    for member in inspect.getmembers(self):
                        if member[0] == self.events[event][0]:
                            self.kernel().log("Calling method (%s)" % event)
                            func = member[1]
                            if len(inspect.getargspec(func)[0]) > 2:
                                func(match, msg)
                            elif len(inspect.getargspec(func)[0]) > 1:
                                func(match)
                            else:
                                func()

        self.messages = []

    def parse_menu(self):
        header = self.kernel().get_row_line(0)
        skip_first = len(header) - len(header.lstrip())

        # What to pick up menu
        if header and header.find("Pick up what?") >= 0:
            # choose all armors to inventory
            choice = []
            is_armor = False
            for i in range(1, TTY_HEIGHT+1):
                row = self.kernel().get_row_line(i)[skip_first:]
                if 'Armor' in row:
                    is_armor = True
                    continue

                if is_armor:
                    if row[0].islower():
                        choice.append(row[0])
                    else:
                        break

            self.kernel().curTile().items = []
            self.kernel().log(f'Pick up what choice: {choice}')
            self.kernel().send(''.join(choice) + '\r')

        else:
            self.kernel().send(' ')
