from nethack_raph.myconstants import OBJECT_CLASSES as OCLASSES

from collections import Counter
import numpy as np


class Inventory:
    def __init__(self, kernel):
        self.kernel = kernel
        self.raw_glyphs = np.array((), dtype=np.int16)
        self.inv_strs = None
        self.inv_letters = None
        self.inv_oclasses = np.array((), dtype=np.int16)
        self.inv_glyphs = np.array((), dtype=np.int16)
        self.new_weapons = []
        self.new_armors = []
        self.take_off_armors = []
        self.being_worn_count = None

    def update(self, obs):
        self.raw_glyphs = np.copy(obs['inv_glyphs'])

        # parse the inventory
        inv_letters = obs['inv_letters'].view('c')  # uint8 to bytes
        index, = inv_letters.nonzero()  # keep non-empty slots only
        inv_strs = obs['inv_strs'].view('S80')[:, 0]  # uint8 to sz

        if (self.inv_oclasses == OCLASSES['WEAPON_CLASS']).sum() < (obs['inv_oclasses'][index] == OCLASSES['WEAPON_CLASS']).sum():
            for oc, glyph, inv_str, letter in zip(
                    obs['inv_oclasses'][index],
                    obs['inv_glyphs'][index],
                    inv_strs[index].astype(str),
                    inv_letters[index].astype(str)):
                if oc == OCLASSES['WEAPON_CLASS'] and not 'in hand' in inv_str:
                    self.new_weapons.append((glyph, inv_str, letter))

        if (self.inv_oclasses == OCLASSES['ARMOR_CLASS']).sum() < (obs['inv_oclasses'][index] == OCLASSES['ARMOR_CLASS']).sum():
            for oc, glyph, inv_str, letter in zip(
                    obs['inv_oclasses'][index],
                    obs['inv_glyphs'][index],
                    inv_strs[index].astype(str),
                    inv_letters[index].astype(str)):
                if oc == OCLASSES['ARMOR_CLASS'] and not 'being worn' in inv_str:
                    self.new_armors.append((glyph, inv_str, letter))

        self.being_worn_count = len([oc for oc, inv_str in zip(obs['inv_oclasses'][index], inv_strs[index].astype(str))
                                     if oc == OCLASSES['ARMOR_CLASS'] and 'being worn' in inv_str])

        self.inv_strs = inv_strs[index].astype(str)  # convert to utf8 strings
        self.inv_letters = inv_letters[index].astype(str)
        self.inv_oclasses = obs['inv_oclasses'][index]
        self.inv_glyphs = obs['inv_glyphs'][index]

    def have_food(self):
        return bool((self.inv_oclasses == OCLASSES['FOOD_CLASS']).sum())
