from nethack_raph.myconstants import directions


class Cursor:
    def __init__(self, kernel):
        self.started = True
        self.y = 0
        self.x = 0
        self.kernel = kernel

    def start(self):
        self.started = True
        self.y = self.kernel().hero.y
        self.x = self.kernel().hero.x

        self.kernel().log("Cursor starts at (%d,%d)" % (self.y, self.x))

    def draw(self):
        self.kernel().stdout("\x1b[%d;%df" % (self.y+2, self.x+1))

    def input(self, char):
        if char not in ['y','u','h','j','k','l','b','n','.']:
            return
        if char == '.':
            pass
        else:
            dir = directions[char]
            self.y = self.y + dir[0]
            self.x = self.x + dir[1]
            self.kernel().drawString(str(self.kernel().dungeon.tile(self.y, self.x)))
            self.draw()
