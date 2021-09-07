import re
from nethack_raph.EeekObject import *


class Inventory(EeekObject):
    def __init__(self):
        EeekObject.__init__(self)
        items = []

    def search(self, what, getFirst=False):
        ret = []
        for item in items:
            count = 0
            for find in what:
                if find in item.__dict__ and item.__dict__[find].find(what[find])>=0:
                    if getFirst:
                        return item
                    count = count + 1
            if count == len(what):
                ret.append(item)
        return len(ret)==1 and ret[0] or ret

    def add(self, item):
        if item not in self.items:
            self.items.append(item)

    def parseFrame(self, match):
        first = match.groups()[0]
        (row, start) = (1, self.kernel().FramebufferParser.topLine().find(first))

        while True:
            line = self.kernel().FramebufferParser.getRowLine(row)
            if line.find("(end)") != -1:
                break

            if line[start+1] == ' ':
                self.kernel().log(line)
                match = re.search("(\w) - (a|an|\d+)( (uncursed|cursed|blessed)|)( (\+\d+|-\d+|)|) (.+)( \((.+)\)|)", line)
                if match:
                    self.kernel().log(str(match.groups()))
                    (slot, qty, trash, buc, trash, enchant, item, trash, info) = map(lambda x:x and x.strip(), match.groups())
                    it = Item()
                    self.kernel().Inventory.add
                else:
                    self.kernel().die("Unparsed inventory item: %s" % line)

            row = row + 1
        self.kernel().send(" ")
