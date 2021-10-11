from nethack_raph.Actions.base import BaseAction
from nethack_raph.myconstants import COLOR_BG_RED

import numpy as np


class RangeAttackMonster(BaseAction):
    def __init__(self, kernel):
        self.weapon_letter = None
        self.attack_direction = None
        super().__init__(kernel)

    def get_way_(self, array, start, end):
        """
        Returns slice with tiles on the way from point start to point end.
        start and end should be on the same horizontal / vertical or diagonal

        Parameters
        ----------
        array : array_like,
        start : tuple[int, int]
            start point
        end : tuple[int, int]
            end point

        Returns
        -------
        array-like - tiles on the way from point start to point end

        Raises
        ------
        RuntimeError
            when start and end aren't on the same horizontal, vertical or diagonal
        """

        assert start != end

        start_x, start_y = start
        end_x, end_y = end

        if start_x == end_x:  # horizontal
            if start_y < end_y:
                return array[start_x, start_y: end_y + 1]
            else:
                return array[start_x, end_y: start_y + 1][::-1]

        elif start_y == end_y:  # vertical
            if start_x < end_x:
                return array[start_x: end_x + 1, start_y]
            else:
                return array[end_x: start_x + 1, start_y][::-1]

        elif abs(start_x - end_x) == abs(start_y - end_y):  # diagonal
            length = abs(start_x - end_x) + 1
            if (start_x - end_x) * (start_y - end_y) > 0:  # our way is parallel to main diagonal
                if start_x < end_x:
                    return np.diagonal(array[start_x:, start_y:])[:length]
                else:
                    return np.diagonal(array[end_x:, end_y:])[length-1::-1]

            else:  # our way is parallel to main anti-diagonal
                if start_x < end_x:
                    return np.diagonal(np.fliplr(array[start_x:, :start_y + 1]))[:length]
                else:
                    return np.diagonal(np.fliplr(array[end_x:, :end_y + 1]))[length-1::-1]

        else:
            raise RuntimeError

    def can(self, level):
        if not self.kernel().hero.use_range_attack:
            return False, None

        self.weapon_letter = self.kernel().inventory.range_weapon()
        if self.weapon_letter is None:
            return False, None

        max_range = min(self.hero.strength // 2, 12)
        monsters = []
        for xy, monster in level.monsters.items():
            if monster is None or (not monster.is_attackable and not monster.passive):
                continue

            if xy[0] != self.hero.x and xy[1] != self.hero.y \
                    and abs(xy[0] - self.hero.x) != abs(xy[1] - self.hero.y):
                continue  # not on the same row, file or diagonal

            distance = max(abs(c - h) for c, h in zip(xy, self.hero.coords()))
            if monster.passive and distance == 1:
                continue  # don't attack passive monster nearby

            if self.hero.prefer_melee_attack and distance == 1:
                continue

            if distance > max_range:
                continue  # too far away from us

            way = self.get_way_(level.tiles, self.hero.coords(), xy)
            if not way[1:-1].walkable_glyph.all():
                continue

            monster_on_the_way = False
            for tile in way[1:-1]:
                if tuple(tile.xy) in level.monsters:
                    monster_on_the_way = True
                    break

            if monster_on_the_way:
                continue

            dir = tuple(way[1].xy)
            monsters.append((dir, distance))
            self.log(f'Range attack available to {dir} to distance: {distance}')

        if not monsters:
            return False, None
        else:
            self.attack_direction, _ = min(monsters, key=lambda x: x[1])  # attack the closest monster
            return True, None

    def execute(self, path=None):
        assert path is None
        self.log(f'Range attack {self.attack_direction}')
        self.hero.throw(self.attack_direction, self.weapon_letter)
