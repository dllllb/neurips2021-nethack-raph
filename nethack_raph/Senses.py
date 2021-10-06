from nethack_raph.myconstants import TTY_HEIGHT, DUNGEON_WIDTH

import inspect
import re


class Senses:
    def __init__(self, kernel):
        self.kernel = kernel
        self.messages = []

        self.events = {
            # "(needs food, badly!|feel weak now\.|feel weak\.)":              ['is_weak'],
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
            ".*elcome to .* (store|dealership|bookstore|emporium|"
                "outlet|delicatessen|jewelers|accessories|hardware|"
                "books|food|lighting).*":                                    ['shop_entrance'],
            "You can't move diagonally into an intact doorway.":             ['open_door_there'],
            "You can't move diagonally out of an intact doorway.":           ['open_door_here'],
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

            # r".* eat it\? \[ynq\] \(n\)":                                    ['eat_it'],
            "You see no door there.":                                        ['no_door'],
            "You finish eating .*":                                          ['food_is_eaten'],
            "You harmlessly attack a statue.":                               ['is_statue'],
            "You cannot pass through the bars.":                             ['not_walkable'],
            "You are carrying too much to get through.":                     ['not_walkable'],
            "Hello stranger, who are you?":                                  ['who_are_you'],
            "It's solid stone.":                                             ['not_walkable'],
            "Will you please leave your (.*) outside\?":                     ['leave_pick'],
            "Call a scroll .*":                                              ['scroll'],
            "You don't have anything to eat.":                               ['no_food'],
            "You don't have anything else to wear.":                         ['no_wear'],
            "You don't have anything else to put on.":                       ['no_wear'],
            "Call a scroll labeled .*":                                      ['read_scroll'],
            "(.+) engulfs you":                                              ['got_engulfed'],
            "Call (.+) potion":                                              ['call_potion'],
            "You kill .*":                                                   ['killed_monster'],
            "Continue eating\? .*":                                          ['stop_eating'],
            "You see no objects here.":                                      ['nothing_found'],
            "You can't write on the .*":                                     ['cant_write'],
            "You are hit.*":                                                 ['you_was_hit'],
            "There is nothing here to pick up.":                             ['no_pickup'],
            "The stairs are solidly fixed to the floor.":                    ['no_pickup'],
            "You could drink the water...":                                  ['no_pickup'],
            "You cannot wear .*":                                            ['cant_wear'],
            "You are already wearing .*":                                    ['cant_wear'],
            "[a-z] - ":                                                      ['picked_up'],
            "You finish your dressing maneuver.":                            ['dressed'],
            "You finish taking off your mail.":                              ['took_off'],
            r".*rop.*gold.*":                                                ['drop_gold']
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

        #TODO MOVE THE ABOWE TO UPDATE

        if self.kernel().searchTop("In what direction?"):
            self.kernel().log("Getting rid if 'In what direction?' prompt")
            self.kernel().send("\x1b")

        match = self.kernel().searchTop(r"What do you want to eat\? \[(.*) or \?\*\]")
        if match:
            self.what_to_eat(match)
            return

        elif self.kernel().searchTop(r".* eat .*\? \[ynq\] \(n\)"):
            self.eat_it(message=self.kernel().top_line())
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
        elif self.kernel().searchTop("Really attack the guard\? \[yn\] \(n\)"):
            self.kernel().send('n')
            return
        if self.kernel().searchTop("Really attack"):
            self.kernel().log("Asked if I really want to attack.")
            self.kernel().send("y")
            return

        elif self.kernel().searchTop("\? \[(.*?)\]"):
            self.kernel().log("Found a prompt we can't handle: %s" % self.kernel().top_line())
            self.kernel().send(" ")

    def drop_gold(self, *, match=None, message=None):
        self.kernel().send('d$')

    def got_expelled(self, *, match=None, message=None):
        self.kernel().log("Got expelled. Phew!")
        self.kernel().hero.isEngulfed = False

    def got_engulfed(self, *, match, message=None):
        self.kernel().log("We just got engulfed. This will confuze me a whole lot :(")
        self.kernel().hero.isEngulfed = True

    def shopkeep_door(self, *, match=None, message=None):
        neighbours = self.kernel().curLevel().neighbours[self.kernel().hero.coords()]
        neighbours.shopkeep_door[neighbours.is_closed_door] = True

    def locked_door(self, *, match=None, message=None):
        if self.kernel().hero.lastActionedTile is None:
            return

        tile = self.kernel().curLevel().tiles[self.kernel().hero.lastActionedTile]
        if tile.is_closed_door:
            tile.locked = True

    def found_trap(self, type, *, match=None, message=None):
        self.kernel().log("I found a trap. Setting char to ^")
        self.kernel().curLevel().set_as_trap(self.kernel().curTile())

    def fell_into_pit(self, *, match=None, message=None):
        self.kernel().log("I fell into a pit :(")
        self.kernel().hero.inPit = True
        self.kernel().curLevel().set_as_trap(self.kernel().curTile())

    def found_beartrap(self, *, match=None, message=None):
        self.kernel().log("Found a beartrap. Setting tile to ^")
        self.kernel().curLevel().set_as_trap(self.kernel().curTile())

    def stepped_in_beartrap(self, *, match=None, message=None):
        self.kernel().log("Just stepped into a beartrap :(")
        self.kernel().hero.inBearTrap = True
        self.kernel().curLevel().set_as_trap(self.kernel().curTile())

    def trigger_trap(self, *, match=None, message=None):
        self.kernel().log("Triggered a trap, setting char to ^.. Not changing color yet")
        self.kernel().curLevel().set_as_trap(self.kernel().curTile())

    def blinded(self, *, match=None, message=None):
        self.kernel().log("I got blinded.")
        self.kernel().hero.blind = True

    def gain_instrinct(self, type, *, match=None, message=None):
        pass

    def skill_up(self, *, match, message=None):
        if match.groups()[0] == 'weapon':
            self.kernel().log("Enhanced weaponskill!")
            pass

    def open_door_here(self, *, match=None, message=None):
        tile = self.kernel().curLevel().tiles[self.kernel().hero.coords()]
        if not tile.is_opened_door:
            self.kernel().curLevel().set_as_door(tile)

    def open_door_there(self, *, match=None, message=None):
        tile = self.kernel().curLevel().tiles[self.kernel().hero.lastActionedTile]
        if not tile.is_opened_door:
            self.kernel().curLevel().set_as_door(tile)

    def call_potion(self, *, match, message=None):
        self.kernel().send("\x1b")

    def eat_it(self, *, match=None, message):
        if self.kernel().hero.lastAction == 'eat_from_inventory':
            self.kernel().log('eating from inventory. eating aborted')
            self.kernel().send('n')
            return

        if not all([item.is_food for item in self.kernel().curLevel().items[self.kernel().hero.coords()] if item.char == '%']):
            # otherwise we should check that food in msg correspond to edible food
            self.kernel().log('not edible: eating aborted')
            self.kernel().send('n')
            for item in self.kernel().curLevel().items[self.kernel().hero.coords()]:
                if item.char == '%':
                    item.is_food = False
            return

        if 'corpse' in message and not bool([item.is_food for item in self.kernel().curLevel().items[self.kernel().hero.coords()] if item.corpse]):
            self.kernel().log('unknown / not edible corpse: eating aborted')
            self.kernel().send('n')
            for item in self.kernel().curLevel().items[self.kernel().hero.coords()]:
                if item.char == '%':
                    item.is_food = False
            return

        self.kernel().log('eating...')
        self.kernel().send('y')

    def no_door(self, *, match=None, message=None):
        if self.kernel().hero.lastActionedTile:
            tile = self.kernel().curLevel().tiles[self.kernel().hero.lastActionedTile]
            tile.is_closed_door = False

    def what_to_eat(self, matched):
        options = matched.groups()[0]
        self.kernel().log('eating...' + options)
        if 'f' in options:
            self.kernel().send('f')
        else:
            self.kernel().send(options[0])

    def is_displeased(self, *, match=None, message=None):
        self.kernel().hero.god_is_angry = True

    def is_staircase_here(self, *, match, message=None):
        self.kernel().log("Found staircase under some items..")

        if match.groups()[0] == 'down':
            self.kernel().curTile().char = '>'
        else:
            self.kernel().curTile().char = '<'

    def leg_no_shape(self, *, match=None, message=None):
        #TODO DONT WORK
        self.kernel().log("Leg is not in shape :'(")
        self.kernel().hero.legShape = False

    def leg_feels_better(self, *, match=None, message=None):
        self.kernel().log("Leg is fine again.")
        self.kernel().hero.legShape = True

    def found_items(self, *, match, message):
        self.kernel().log("Found some item(s)..")

    def shop_entrance(self, *, match, message):
        # TODO (level refactor)
        self.kernel().log("Found a shop.")

        if self.kernel().curTile().is_opened_door and self.kernel().hero.lastAction == 'move':
            prev_coords = self.kernel().hero.beforeMove
            cur_coords = self.kernel().hero.coords()
            # entrance is opposite to the tile where we came from
            entrance_x, entrance_y = tuple((2*c - p) for c, p in list(zip(cur_coords, prev_coords)))
            entrance_tile = self.kernel().curLevel().tiles[entrance_x, entrance_y]

            entrance_tile.shop_entrance = True
            self.kernel().curLevel().update_walk_cost(entrance_tile)
            self.kernel().log(f'Shop entrance: {entrance_tile}')

        buf = [self.kernel().curTile()]
        while buf:
            for tile in self.kernel().curLevel().get_neighbours(buf.pop()):
                # This could break once a year or so (if a monster is standing in a non-shop square after you login?)
                x, y = tile.xy
                is_monster = bool(self.kernel().curLevel().monsters[x, y]) and not self.kernel().curLevel().monsters[x, y].pet
                is_item = bool(self.kernel().curLevel().items[x, y])
                if (tile.char == '.' or is_monster or is_item) and not tile.in_shop:
                    buf.append(tile)
                    self.kernel().log("Setting %s to be inside a shop." % tile)
                    self.kernel().curLevel().tiles[x, y].in_shop = True

    def food_is_eaten(self, *, match=None, message=None):
        pass

    def no_food(self, *, match=None, message=None):
        for item in self.kernel().curLevel().items[self.kernel().hero.coords()]:
            if item.char == '%':
                item.is_food = False

    def stop_eating(self, *, match=None, message):
        # probably ate something wrong
        self.kernel().log('not edible: eating aborted')
        self.kernel().send('n')
        for item in self.kernel().curLevel().items[self.kernel().hero.coords()]:
            if item.char == '%':
                item.is_food = False

    def no_wear(self, *, match=None, message=None):
        self.kernel().inventory.new_armors = []

    def read_scroll(self, *, match=None, message=None):
        self.kernel().send('r\r') # 'r\r' seems to work

    def is_statue(self, *, match=None, message=None):
        if self.kernel().hero.lastActionedTile and self.kernel().curLevel().monsters[self.kernel().hero.lastActionedTile]:
            self.kernel().curLevel().monsters[self.kernel().hero.lastActionedTile].is_statue = True

    def not_walkable(self, *, match=None, message=None):
        if self.kernel().hero.lastActionedTile:
            tile = self.kernel().curLevel().tiles[self.kernel().hero.lastActionedTile]
            tile.walkable_glyph = False
            self.kernel().curLevel().update_walk_cost(tile)

    def leave_pick(self, *, match, message=None):
        pass

    def who_are_you(self, *, match=None, message=None):
        # XXX dubious strategy... failed for a vutpurse in a vault on level 1
        self.kernel().send('Croseus\r')

    def scroll(self, *, match=None, message=None):
        self.kernel().send('r')

    def carrying_too_mach(self):
        # FIXME (dima) drop smth
        if self.kernel().hero.lastActionedTile:
            tile = self.kernel().curLevel().tiles[self.kernel().hero.lastActionedTile]
            tile.walkable_glyph = False
            self.kernel().curLevel().update_walk_cost(tile)

    def graffiti_on_floor(self, *, match=None, message=None):
        self.kernel().log("Found grafitti!")

    def killed_monster(self, *, match, message):
        if self.kernel().hero.lastActionedTile is None:
            return

        for item in self.kernel().curLevel().items[self.kernel().hero.lastActionedTile]:
            if item.corpse and item.corpse in message and item.turn_of_death < 0:
                item.turn_of_death = self.kernel().hero.turns

    def you_read(self, *, match, message=None):
        self.kernel().log(f'YOU READ {match.groups()[0]}')
        self.kernel().curTile().has_elbereth = match.groups()[0] == 'Elbereth'

    def nothing_found(self, *, match=None, message=None):
        self.kernel().curLevel().clear_items(*self.kernel().hero.coords())

    def cant_write(self, *, match=None, message=None):
        if self.kernel().curTile().char == '':
            self.kernel().curTile().char = '{'

    def you_was_hit(self, *, match=None, message=None):
        if self.kernel().curTile().has_elbereth:
            # you was hit, possible from distance, elbereth doesn't protect you
            for monster in self.kernel().curLevel().monsters.values():
                if monster and not monster.pet:
                    monster.range_attack = True

    def no_pickup(self, *, match=None, message=None):
        self.kernel().curLevel().clear_items(*self.kernel().hero.coords())

    def picked_up(self, *, match=None, message=None):
        self.kernel().curLevel().clear_items(*self.kernel().hero.coords())

    def dressed(self, *, match=None, message=None):
        if self.kernel().hero.armor_class >= self.kernel().hero.armor_class_before:
            self.kernel().inventory.take_off_armors.append(self.kernel().hero.lastActionedItem)

    def took_off(self, *, match=None, message=None):
        # Drop unused item:
        self.kernel().log(f'Drop item {self.kernel().hero.lastActionedItem}')
        self.kernel().send(f'd{self.kernel().hero.lastActionedItem}')
        self.kernel().curTile().dropped_here = True

    def cant_wear(self, *, match=None, message=None):
        # Drop unused item:
        self.kernel().log(f'Drop item {self.kernel().hero.lastActionedItem}')
        self.kernel().send(f'd{self.kernel().hero.lastActionedItem}')
        self.kernel().curTile().dropped_here = True
        # TODO (nikita): we can try take off another item, if we are already wearing that type of armor

    def parse_messages(self):
        members = dict(inspect.getmembers(self))

        for msg in self.messages:
            for event, (handler, *args) in self.events.items():
                match = re.search(event, msg)
                if not match:
                    continue

                self.kernel().log("Found message: %s" % event)
                if handler in members:
                    self.kernel().log("Calling method (%s)" % event)
                    members[handler](*args, match=match, message=msg)

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

            self.kernel().curLevel().clear_items(*self.kernel().hero.coords())
            self.kernel().log(f'Pick up what choice: {choice}')
            self.kernel().send(''.join(choice) + '\r')

        elif header and header.find("attributes:") >= 0:  # parsing agent's attributes at the start
            msg = self.kernel().get_row_line(3) + self.kernel().get_row_line(4)
            self.kernel().hero.set_attributes(msg)
            self.kernel().send('  ')

        elif header and header.find("There is an open door here") >= 0:
            self.open_door_here()
            self.kernel().send(' ')
        else:
            self.kernel().send(' ')
