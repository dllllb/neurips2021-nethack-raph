from nethack_raph.Kernel import Kernel
from nethack_raph.myconstants import DUNGEON_HEIGHT, DUNGEON_WIDTH
from nethack_raph.Actions.RLTriggerAction import RLTriggerAction

import gym
import numpy as np
from nle import nethack as nh
from nle.nethack.actions import ACTIONS


class RLWrapper(gym.Wrapper):
    def __init__(self, env, verbose=False):
        super().__init__(env)
        self.verbose = verbose
        self.kernel = Kernel(verbose=self.verbose)

        self.action_space = gym.spaces.Discrete(18)
        self.action2id = {
            chr(action.value): action_id for action_id, action in enumerate(ACTIONS)
        }

        self.episode_reward = 0
        self.offsets = [(-1, 0), (1, 0), (0, -1), (0, 1), (-1, -1), (-1, 1), (1, -1), (1, 1)]
        self.is_corner = [False, False, False, False, True, True, True, True]
        self.roles = np.array(['arc', 'bar', 'cav', 'hea', 'kni', 'mon', 'pri', 'ran', 'rog', 'sam', 'tou', 'val', 'wiz'])
        self.races = np.array(['dwa', 'elf', 'gno', 'hum', 'orc'])
        self.genders = np.array(['fem', 'mal'])
        self.morals = np.array(['cha', 'law', 'neu'])
        self.last_obs = None
        self.reward = 0

        self.actionid2name = {-1: 'Continue'}
        for i in range(8):
            self.actionid2name[i] = 'AttackMonster'
        for i in range(8, 16):
            self.actionid2name[i] = 'RangeAttackMonster'
        self.actionid2name[16] = 'Wait'
        self.actionid2name[17] = 'Elbereth'

    def reset(self):
        self.reward = 0
        del self.kernel
        self.kernel = Kernel(verbose=self.verbose)
        self.last_obs = self.env.reset()
        self.kernel.update(self.last_obs)
        _, _, done, _ = self._step()
        if done:
            return self.reset()
        return self._process_obs(self.last_obs, rl_triggered=False)

    def step(self, action_id):
        self.reward = 0

        action_id = int(action_id)
        action_name = self.actionid2name[action_id]
        if action_name in ('AttackMonster', 'RangeAttackMonster'):
            x, y = self.kernel.hero.coords()
            tile_x, tile_y = self.offsets[action_id % 8]
            tile = (tile_x + x, tile_y + y)
            self.kernel.brain.rl_actions[action_name].execute(tile)
        elif action_name in ('Wait', 'Elbereth'):
            self.kernel.brain.rl_actions[action_name].execute()
        else:
            action, path = self.kernel.brain.execute_next(self.kernel.curLevel())
            if isinstance(action, RLTriggerAction):
                return self._process_obs(self.last_obs, rl_triggered=True), self.reward, False, {}
            action.execute(path)

        assert len(self.kernel.action) > 0
        self.last_obs, _, done, info = self._step()
        return self._process_obs(self.last_obs, rl_triggered=False), self.reward, done, info

    def _step(self):
        done, info = False, {}
        while not done and self.kernel.action:
            self.last_obs, rew, done, info = self.env.step(self.action2id.get(self.kernel.action[0]))
            self.reward += rew
            self.kernel.action = self.kernel.action[1:]
            if self.kernel.action:
                continue
            self.kernel.update(self.last_obs)

        info['role'] = self.kernel.hero.role
        return self.last_obs, self.reward, done, info

    def _process_obs(self, obs, rl_triggered):
        state = np.zeros((16, DUNGEON_HEIGHT, DUNGEON_WIDTH), dtype=np.int32)
        action_mask = np.zeros(self.action_space.n, dtype=np.float32)

        if not rl_triggered:
            return {
                'map': state,
                'message': obs['message'],
                'blstats': obs['blstats'],
                'action_mask': action_mask,
                'hero_stat': np.zeros(23),
                'rl_triggered': rl_triggered,
            }

        lvl = self.kernel.curLevel()
        tiles = lvl.tiles
        state[0] = tiles.explored
        state[1] = tiles.walkable_tile
        state[2] = tiles.walkable_glyph
        state[3] = tiles.is_hero
        state[4] = tiles.is_opened_door
        state[5] = tiles.is_closed_door
        state[6] = tiles.in_shop
        state[7] = tiles.shop_entrance
        state[8] = tiles.locked
        state[9] = tiles.has_elbereth

        for (x, y), monster in lvl.monsters.items():
            state[10, x, y] = True
            state[11, x, y] = monster.is_attackable
            if monster.glyph < 381:
                mon_info = nh.permonst(nh.glyph_to_mon(monster.glyph))
                state[12, x, y] = mon_info.ac
                state[13, x, y] = mon_info.mlevel
                state[14, x, y] = mon_info.mmove

        x, y = self.kernel.hero.coords()
        doors = lvl.tiles.is_opened_door

        for i, off in enumerate(self.offsets):
            tile = (x + off[0], y + off[1])
            if tile[0] < 0 or tile[0] >= DUNGEON_HEIGHT or tile[1] < 0 or tile[1] >= DUNGEON_WIDTH:
                continue

            if tile in lvl.monsters:
                action_mask[i] = 1.0

            if self.is_corner[i] and (doors[tile] or doors[(x, y)]):
                continue

            if tiles[tile].walkable_tile:
                action_mask[i] = 1.0

        if self.kernel.brain.rl_actions['RangeAttackMonster'].can(lvl)[0]:
            action_mask[8:16] = 1.0
        if True:  # can wait
            action_mask[16] = 1.0
        if self.kernel.brain.rl_actions['Elbereth'].can(lvl)[0]:
            action_mask[17] = 1.0

        hero_stat = np.concatenate([
            self.kernel.hero.role == self.roles,
            self.kernel.hero.race == self.races,
            self.kernel.hero.gender == self.genders,
            self.kernel.hero.moral == self.morals
        ]).astype(np.float32)

        return {
            'map': state,
            'message': obs['message'],
            'blstats': obs['blstats'],
            'action_mask': action_mask,
            'hero_stat': hero_stat,
            'rl_triggered': rl_triggered,
            'inventory': np.array([self.kernel.inventory.range_weapon() is not None])
        }
