import sys


class Console:
    def __init__(self, kernel):
        self.buf = []
        self.line = ""
        self.kernel = kernel

    def input(self, char):
        if char == "|":
            pass
        elif char == "!":
            self.line = "self.kernel()."
        elif char == "\x10":
            if len(self.buf)>1:
                self.line = self.buf[-2][2:]
        elif char == "\n":
            if self.line == "quit":
                self.kernel().send("\x1b\x1b#quit\ny        ")
                self.kernel().die("Quitted from console")
            if self.line == "save":
                self.kernel().send("\x1b\x1bSy      ")
                self.kernel().die("Saved from console")
            self.buf.append("> %s" % self.line)
            try:
                res = str(eval(self.line))
                if len(res) > 0:
                    self.buf.append(res)
                else:
                    self.buf.append("OK.")
            except:
                err = ",".join(map(str, sys.exc_info()))
                self.buf.append(err)
            self.line = ""
        elif char == '\x7f':
            self.line = self.line[:-1]
        else:
            self.line = self.line + char

    def draw(self):
        self.kernel().stdout("\x1b[16;80H\x1b[1J\x1b[37m")
        self.kernel().stdout("\x1b[16;1H")
        self.kernel().stdout('-' * 80)
        self.kernel().stdout("\x1b[1;1;H")


        printed = 1
        for line in self.buf[-14:]:
            self.kernel().stdout(line)
            self.kernel().stdout("\x1b[1E")

        self.kernel().stdout("> %s" % self.line)

