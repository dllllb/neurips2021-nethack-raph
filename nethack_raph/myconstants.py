TTY_WIDTH = 80
TTY_HEIGHT = 24

DUNGEON_WIDTH = 79
DUNGEON_HEIGHT = 21
TTY_BRIGHT = 8
RL_VIEW_DISTANCE = 4

GOAL_SOKOBAN         = 0
GOAL_MINETOWN        = 1
GOAL_MINESEND        = 2

WHEREIS_MINES        = range(2, 5)
WHEREIS_MINETOWN     = range(5, 9)
WHEREIS_MINESEND     = range(10, 14)
WHEREIS_ORACLE       = range(5, 10)
WHEREIS_SOKOBAN      = range(6, 11)
WHEREIS_QUEST        = range(11, 17)
WHEREIS_GEHENNOM     = range(32, 38) # TODO

COLOR_BLACK          = 30
COLOR_RED            = 31
COLOR_GREEN          = 32
COLOR_YELLOW         = 33
COLOR_BLUE           = 34
COLOR_MAGENTA        = 35
COLOR_CYAN           = 36
COLOR_WHITE          = 37

COLOR_BROWN          = 38
COLOR_GRAY           = 39
COLOR_NONE           = 40
COLOR_ORANGE         = 41
COLOR_BRIGHT_GREEN   = 42
COLOR_BRIGHT_BLUE    = 43
COLOR_BRIGHT_MAGENTA = 44
COLOR_BRIGHT_CYAN    = 45

COLOR_BG_BLACK      = 40
COLOR_BG_RED        = 41
COLOR_BG_GREEN      = 42
COLOR_BG_YELLOW     = 43
COLOR_BG_BLUE       = 44
COLOR_BG_MAGENTA    = 45
COLOR_BG_CYAN       = 46
COLOR_BG_WHITE      = 47
COLOR_BG_BLACK      = 48

directions = {  'y': [-1, -1],
                'u': [-1,  1],
                'h': [ 0, -1],
                'k': [-1,  0],
                'j': [ 1,  0],
                'l': [ 0,  1],
                'b': [ 1, -1],
                'n': [ 1,  1]
                }

OBJECT_CLASSES = {
    'RANDOM_CLASS': 0,
    'ILLOBJ_CLASS': 1,
    'WEAPON_CLASS': 2,
    'ARMOR_CLASS':  3,
    'RING_CLASS':   4,
    'AMULET_CLASS': 5,
    'TOOL_CLASS':   6,
    'FOOD_CLASS':   7,
    'POTION_CLASS': 8,
    'SCROLL_CLASS': 9,
    'SPBOOK_CLASS': 10,
    'WAND_CLASS':   11,
    'COIN_CLASS':   12,
    'GEM_CLASS':    13,
    'ROCK_CLASS':   14,
    'BALL_CLASS':   15,
    'CHAIN_CLASS':  16,
    'VENOM_CLASS':  17
}
