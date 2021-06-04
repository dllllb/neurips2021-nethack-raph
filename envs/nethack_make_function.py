import aicrowd_gym
import nle

def nethack_make_fn():
    return aicrowd_gym.make('NetHackChallenge-v0',
                    observation_keys=("glyphs",
                                    "chars",
                                    "colors",
                                    "specials",
                                    "blstats",
                                    "message",
                                    "tty_chars",
                                    "tty_colors",
                                    "tty_cursor",))