from nethack_raph.glossaries.ArmorGlossary import ARMOR_GLOSSARY
from nethack_raph.glossaries.MonsterGlossary import MONSTERS_GLOSSARY
from nethack_raph.glossaries.WeaponGlossary import WEAPON_GLOSSARY

throw_skills = {'dart', 'shuriken', 'spear', 'dagger', 'knife'}
ITEMS_TO_THROW = {k for k, v in WEAPON_GLOSSARY.items() if v['skill'] in throw_skills}

melee_skills = {
    'flail', 'dagger', 'hammer', 'knife', 'long sword', 'short sword', 'morning star',
    'spear', 'trident', 'two-handed sword', 'whip', 'axe', 'broadsword', 'club',
    'lance', 'pick-axe', 'mace', 'polearms', 'quarterstaff', 'saber', 'scimitar'
}

exclude = {'boomerang', 'bow', 'dart', 'shuriken', 'sling', 'crossbow'}

MELEE_WEAPON = {k for k, v in WEAPON_GLOSSARY.items() if v['skill'] in melee_skills}
