import numpy as np

from nethack_raph.Actions.base import BaseAction


class RandomWalk(BaseAction):
    def can(self, level):
        targets = level.tiles.walkable_tile & \
            (level.tiles.char == '.') & \
            ~level.tiles.visited & \
            ~level.tiles.is_hero & \
            ~level.tiles.in_shop

        return targets.any(), targets

    def after_search(self, targets, path):
        if path is None:
            self.kernel().curLevel().tiles.visited = False
        self.hero.search(30)

    def execute(self, path):
        *tail, one = path
        hero = self.hero
        assert one == (hero.x, hero.y)

        if not tail:  # XXX used to raise IndexError
            raise RuntimeError

        self.hero.move(tail[-1])

        # XXX what do we do here?
        level = self.kernel().curLevel()
        queue = [self.kernel().curTile()]
        while queue:
            front = queue.pop()
            if front.char == '.' and not front.visited:
                level.tiles[tuple(front.xy)].visited = True
                queue.extend(level.adjacent(front))
