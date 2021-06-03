import nle

# For your local evaluation, aicrowd_gym is completely identical to gym
import aicrowd_gym

def nethack_make_fn():
    # These settings will be fixed by the AIcrowd evaluator
    # This allows us to limit the features of the environment 
    # that we don't want participants to use during the submission
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