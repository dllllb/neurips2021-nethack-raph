from nethack_raph.myconstants import OBJECT_CLASSES as OCLASSES
from nethack_raph.glossaries import WEAPON_GLOSSARY, ITEMS_TO_THROW

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
        self.healing_potions = []
        self.being_worn_count = None
        self.camera = None
        self.camera_charges = 0

    def update(self, obs):
        self.raw_glyphs = np.copy(obs['inv_glyphs'])

        # parse the inventory
        inv_letters = obs['inv_letters'].view('c')  # uint8 to bytes
        index, = inv_letters.nonzero()  # keep non-empty slots only
        inv_strs = obs['inv_strs'].view('S80')[:, 0][index].astype(str)  # uint8 to sz
        inv_letters = inv_letters[index].astype(str)
        inv_oclasses = obs['inv_oclasses'][index]
        inv_glyphs = obs['inv_glyphs'][index]

        # armors
        if (self.inv_oclasses == OCLASSES['ARMOR_CLASS']).sum() < (inv_oclasses == OCLASSES['ARMOR_CLASS']).sum():
            for oc, glyph, inv_str, letter in zip(inv_oclasses, inv_glyphs, inv_strs, inv_letters):
                if oc == OCLASSES['ARMOR_CLASS'] and not 'being worn' in inv_str:
                    self.new_armors.append((glyph, inv_str, letter))

        # potions
        if (self.inv_oclasses == OCLASSES['POTION_CLASS']).sum() < (inv_oclasses == OCLASSES['POTION_CLASS']).sum():

            query = 'healing'
            potion_mask = inv_oclasses == OCLASSES['POTION_CLASS']
            if potion_mask.any():
                query_mask = np.char.find(inv_strs[potion_mask], query) > 0
                self.healing_potions = inv_letters[potion_mask][query_mask].tolist()
            else:
                self.healing_potions = []

        self.being_worn_count = len([oc for oc, inv_str in zip(inv_oclasses, inv_strs)
                                     if oc == OCLASSES['ARMOR_CLASS'] and 'being worn' in inv_str])

        self.inv_strs = inv_strs
        self.inv_letters = inv_letters
        self.inv_oclasses = inv_oclasses
        self.inv_glyphs = inv_glyphs

    def have_food(self):
        return bool((self.inv_oclasses == OCLASSES['FOOD_CLASS']).sum())

    def range_weapon(self):
        # TODO: weapon skills
        range_weapons = [(l, g) for l, g, s in zip(self.inv_letters, self.inv_glyphs, self.inv_strs) \
                         if g in ITEMS_TO_THROW and 'weapon in hand' not in s]
        if range_weapons:
            range_weapon_letter, _ = max(
                [(l, int(WEAPON_GLOSSARY[g]['damage_S'][1:])) for l, g in range_weapons],
                key=lambda x: -x[1]
            )
            return range_weapon_letter
