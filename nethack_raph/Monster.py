from nethack_raph.TermColor import *
from nethack_raph.glossaries import MONSTERS_GLOSSARY



class Monster:
    peacefuls = {
        ('@', COLOR_WHITE),       # shk
        ('@', COLOR_BRIGHT_BLUE), # oracle
        ('@', COLOR_GRAY),        # watchmen
        ('@', COLOR_GREEN),       # watch captain I think
        ('e', COLOR_BLUE),        # floating eye I think
        ('e', COLOR_GRAY),        # gas spore
    }

    def __init__(self, char, color, glyph, kernel):
        self.char = char
        self.color = color
        self.glyph = glyph
        self.name = "unknown"
        self.is_statue = False
        self.spoiler = {}
        self.kernel = kernel

        self.peaceful = (self.char, self.color.getId()) in Monster.peacefuls
        self.pet = 381 <= self.glyph <= 761
        self.is_monster = self.glyph < 381
        self.respect_elbereth = MONSTERS_GLOSSARY.get(self.glyph, {}).get('elbereth', 1)
        self.range_attack = False
        self.is_attackable = (self.is_monster or self.pet) and not self.peaceful

    def __str__(self):
        return "n:%s, ch:%s, c:%s, g:%s, o:%s" % tuple(map(str, [self.name, self.char, self.color, self.glyph, self.spoiler]))
