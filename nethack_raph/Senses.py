from nethack_raph.TermColor import TermColor

import inspect
import re


class Senses:
    def __init__(self, kernel):
        self.kernel = kernel
        self.messages = []

        self.events = {
            "(needs food, badly!|feel weak now\.|feel weak\.)":              ['is_weak'],
            "There is a staircase (down|up) here":                           ['is_staircase_here'],
            "Your (right|left) leg is in no shape":                          ['leg_no_shape'],
            "Your leg feels somewhat better":                                ['leg_feels_better'],
            "You see here":                                                  ['found_items'],
            "Things that are here":                                          ['found_items'],
            "There are (several|many) objects here":                         ['found_items'],
            "There's some graffiti on the floor here":                       ['graffiti_on_floor'],
            "You read: (.*?)":                                               ['graffiti_on_floor'],
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
            "You return to (human|) form":                                   ['no_poly'],
            "There is a teleportation trap here":                            ['found_trap', 'teleport'],
            # r".* eat it\? \[ynq\] \(n\)":              ['eat_it'],
            "You see no door there.": ['no_door'],
            "You finish eating .*": ['food_is_eaten'],
            "You harmlessly attack a statue.": ['is_statue'],
            "You cannot pass through the bars.": ['not_walkable'],
            "You are carrying too much to get through.": ['not_walkable'],
            "You can't move diagonally into an intact doorway.": ['not_walkable'],
            "You can't move diagonally out of an intact doorway.": ['not_walkable'],
            "Hello stranger, who are you?": ['who_are_you'],
            "It's solid stone.": ['not_walkable'],
            "Will you please leave your (.*) outside\?": ['leave_pick'],
            "Call a scroll .*": ['scroll'],
            "You don't have anything to eat.": ['no_food'],
            "You don't have anything else to wear.": ['no_wear'],
            "You don't have anything else to put on.": ['no_wear'],
            "What do you want to wear? [*]": ['what_to_wear'],
            "Call a scroll labeled .*": ['read_scroll'],
            "You destroy the (.+)": ['no_poly'],
            "(.+) engulfs you": ['got_engulfed'],
            "Call a (.+) potion": ['call_potion'],
            "Hello Agent, welcome to NetHack!": ['start_message'],
            "You kill .*": ["killed_monster"],
        }

    def update(self):
        top = self.kernel().top_line().replace("--More--", "")
        self.messages = self.messages + top.strip().split("  ")
        self.kernel().log(str(self.messages))

        if '--More--' in self.kernel().top_line():
            self.kernel().send(' ')

        if self.kernel().searchTop("Things that are here:"):
            self.kernel().log("Found some items. (Row 3)")
            self.kernel().send("    ")
            self.kernel().dontUpdate()

        elif self.kernel().get_row_line(3).find("Things that are here:") >= 0:
            self.messages.append("Things that are here:")
            self.kernel().log("Found some items (row 3).")
            self.kernel().send("    ")
            self.kernel().dontUpdate()

        if self.kernel().searchTop("Really attack"):
            self.kernel().log("Asked if I really want to attack.")
            self.kernel().send("y")
            self.kernel().dontUpdate()

        #TODO MOVE THE ABOWE TO UPDATE

        if self.kernel().searchTop("In what direction?"):
            self.kernel().log("Getting rid if 'In what direction?' prompt")
            self.kernel().send("\x1b")
            self.kernel().dontUpdate()

        match = self.kernel().searchTop(r"What do you want to eat\? \[(.*) or \?\*\]")
        match2 = self.kernel().searchTop(r".* eat .*\? \[ynq\] \(n\)")
        if match:
            self.eat(match)
        elif match2:
            self.eat_it(self.kernel().top_line())
        elif self.kernel().searchTop("What do you want to wear\? \[\*\]"):
            self.what_to_wear()
        elif self.kernel().searchTop("\? \[(.*?)\]"):
            self.kernel().log("Found a prompt we can't handle: %s" % self.kernel().top_line())
            self.kernel().send(" ")
            self.kernel().dontUpdate()

    def no_poly(self):
        if self.kernel().hero.isEngulfed:
            self.kernel().hero.isPolymorphed = False

    def got_expelled(self):
        self.kernel().log("Got expelled. Phew!")
        self.kernel().hero.isEngulfed = False

    def got_engulfed(self, match):
        self.kernel().log("We just got engulfed. This will confuze me a whole lot :(")
        self.kernel().hero.isEngulfed = True

    def shopkeep_door(self):
        #FIXME exception [tile for tile in self.kernel().curTile().neighbours() if tile.is_door][0]
        for tile in self.kernel().curTile().neighbours():
            if tile.is_door:
                tile.shopkeepDoor = True
                break

    def locked_door(self):
        if self.kernel().hero.lastActionedTile and self.kernel().hero.lastActionedTile.is_door:
            self.kernel().hero.lastActionedTile.locked = True

    def found_trap(self, type):
        self.kernel().log("I found a trap. Setting char to ^")
        self.kernel().curTile().char = '^'

    def fell_into_pit(self):
        self.kernel().log("I fell into a pit :(")
        self.kernel().hero.inPit = True
        self.kernel().curTile().char = '^'

    def found_beartrap(self):
        self.kernel().log("Found a beartrap. Setting tile to ^")
        self.kernel().curTile().char = '^'

    def stepped_in_beartrap(self):
        self.kernel().log("Just stepped into a beartrap :(")
        self.kernel().hero.inBearTrap = True
        self.kernel().curTile().char = '^'

    def trigger_trap(self):
        #TODO
        self.kernel().log("Triggered a trap, setting char to ^.. Not changing color yet")
        self.kernel().curTile().char = '^'

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
        self.kernel().curTile().char = '-'
        self.kernel().curTile().color = TermColor(33, 0, False, False)

    def call_potion(self, match):
        self.kernel().send("\x1b")
        self.kernel().dontUpdate()

    def eat_it(self, msg):
        if 'corpse' in msg:
            self.kernel().log('corpse: eating aborted')
            self.kernel().send('n')
            for item in self.kernel().curTile().items:
                if item.char == '%':
                    item.is_food = False
        else:
            self.kernel().log('eating...')
            self.kernel().send('y')
        # self.kernel().dontUpdate()

    def no_door(self):
        self.kernel().hero.lastActionedTile.is_door = False

    def eat(self, matched):
        options = matched.groups()[0]
        self.kernel().log('eating...' + options)
        if 'f' in options:
            self.kernel().send('f')
        else:
            self.kernel().send(options[0])

    def is_weak(self):
        self.kernel().personality.curBrain.s_isWeak()
        # self.kernel().sendSignal("s_isWeak")

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
        # input('IN STORE ' + msg)
        # self.kernel().set_verbose(True)

        #FIXME (dima) some loop here
        # self.kernel().hero.lastActionedTile.walkable = False
        # return

        buf = [self.kernel().curTile()]
        while buf:
            for tile in buf.pop().neighbours():
                # This could break once a year or so (if a monster is standing in a non-shop square after you login?)
                if (tile.char == '.' or tile.monster or tile.items) and not tile.inShop:
                    buf.append(tile)

                    self.kernel().log("Setting %s to be inside a shop." % tile)
                    tile.inShop = True

    def food_is_eaten(self):
        pass
        # self.kernel().curTile().items = []

    def no_food(self):
        for item in self.kernel().curTile().items:
            if item.char == '%':
                item.is_food = False

    def no_wear(self):
        for item in self.kernel().curTile().items:
            if item.char == '[':
                item.name = 'absent' #FIXME

    def what_to_wear(self):
        action = input('ENTER ACTION\n')
        self.kernel().send(action)

    def read_scroll(self):
        self.kernel().send('r\r') # 'r\r' seems to work

    def is_statue(self):
        self.kernel().log(str(self.kernel().hero.lastActionedTile))
        self.kernel().hero.lastActionedTile.monster.is_statue = True
        self.kernel().log(str(self.kernel().hero.lastActionedTile))

    def not_walkable(self):
        self.kernel().hero.lastActionedTile.walkable = False

    def leave_pick(self, match):
        #FIXME (dima) do i really need do that?
        # self.kernel().send('d' + self.kernel().get_inventory_letter(match.groups()[0]))
        pass

    def who_are_you(self):
        self.kernel().send('Croseus\r')

    def scroll(self):
        self.kernel().send('r')

    def carrying_too_mach(self):
        # FIXME (dima) drop smth
        self.kernel().hero.lastActionedTile.walkable = False

    def intact_doorway(self):
        # FIXME (dima) hack
        self.kernel().hero.lastActionedTile.walkable = False

    def croesus(self):
        # FIXME (dima) or respond croesus?
        self.kernel().hero.lastActionedTile.walkable = False

    def graffiti_on_floor(self):
        self.kernel().log("Found grafitti!")

    def start_message(self):
        msg = ' '.join(self.messages[1:])
        self.kernel().hero.set_attributes(msg)
        self.kernel().log(str(self.messages))

    def killed_monster(self, msg):
        for item in self.kernel().hero.lastActionedTile.items:
            if item.corpse:  # FIXME (nikita) check glyph of killed monster
                item.turn_of_death = self.kernel().hero.turns

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

    def dontUpdate(self):
        self.kernel().log("Someone told the Senses not to update this tick! Probably myself")
        self.updateNext = False
