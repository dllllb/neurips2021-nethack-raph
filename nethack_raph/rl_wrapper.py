from nethack_raph.Kernel import Kernel
from nethack_raph.Pathing import dijkstra_cpp
from nethack_raph.Actions.AttackMonster import AttackMonster
from nethack_raph.Actions.RangeAttackMonster import RangeAttackMonster
from nethack_raph.myconstants import DUNGEON_HEIGHT, DUNGEON_WIDTH

import gym
import numpy as np
from nle import nethack as nh
from nle.nethack.actions import ACTIONS

BLSTAT_NORMALIZATION_STATS = np.array([
    0.0,  # hero col
    0.0,  # hero row
    0.0,  # strength pct
    1.0 / 10,  # strength
    1.0 / 10,  # dexterity
    1.0 / 10,  # constitution
    1.0 / 10,  # intelligence
    1.0 / 10,  # wisdom
    1.0 / 10,  # charisma
    0.0,  # score
    1.0 / 10,  # hitpoints
    1.0 / 10,  # max hitpoints
    0.0,  # depth
    1.0 / 1000,  # gold
    1.0 / 10,  # energy
    1.0 / 10,  # max energy
    1.0 / 10,  # armor class
    0.0,  # monster level
    1.0 / 10,  # experience level
    1.0 / 100,  # experience points
    1.0 / 1000,  # time
    1.0,  # hunger_state
    1.0 / 10,  # carrying capacity
    0.0,  # carrying capacity
    0.0,  # level number
    0.0,  # condition bits
])

# Make sure we do not spook the network
BLSTAT_CLIP_RANGE = (-5, 5)


class RLWrapper(gym.Wrapper):
    def __init__(self, env, verbose=False):
        super().__init__(env)
        self.verbose = verbose
        self.kernel = Kernel(verbose=self.verbose)

        self.action_space = gym.spaces.Discrete(16)
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

    def reset(self):
        self.episode_reward = 0
        del self.kernel
        self.kernel = Kernel(verbose=self.verbose)
        obs = self.env.reset()
        obs, done, can_throw = self.observation(obs)
        if done:
            return self.reset()
        assert not done

        return self._process_obs(obs, can_throw)

    def step(self, action_id):
        walk = action_id < 8
        action_id = action_id % 8
        x, y = self.kernel.hero.coords()
        tile_x, tile_y = self.offsets[action_id]
        tile = (tile_x + x, tile_y + y)
        lvl = self.kernel.curLevel()
        monster = lvl.monsters.get(tile, None)
        if walk:
            if monster and monster.is_attackable:
                self.kernel.hero.attack(tile)
            else:
                self.kernel.hero.move(tile)
        else:
            self.kernel.hero.throw(tile, self.kernel.inventory.range_weapon())

        while self.kernel.action:
            obs, reward, done, info = self.env.step(self.action2id.get(self.kernel.action[0]))
            self.episode_reward += reward
            self.kernel.action = self.kernel.action[1:]

        if not done:
            obs, done, can_throw = self.observation(obs)
        if done:
            can_throw = False
            info['episode'] = {'r': self.episode_reward}
            info['role'] = self.kernel.hero.role

        return self._process_obs(obs, can_throw), reward, done, info

    def _process_obs(self, obs, can_throw):
        state = np.zeros((16, 21, 79), dtype=np.int32)
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

        action_mask = np.zeros(16, dtype=np.float32)

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

        if can_throw:
            action_mask[8:] = 1.0

        hero_stat = np.concatenate([
            self.kernel.hero.role == self.roles,
            self.kernel.hero.race == self.races,
            self.kernel.hero.gender == self.genders,
            self.kernel.hero.moral == self.morals
        ]).astype(np.float32)

        # blstats = obs["blstats"] * BLSTAT_NORMALIZATION_STATS
        # np.clip(
        #     blstats,
        #     BLSTAT_CLIP_RANGE[0],
        #     BLSTAT_CLIP_RANGE[1],
        #     out=blstats
        # )

        return {
            'map': state,
            'message': obs['message'],
            'blstats': obs['blstats'],
            'action_mask': action_mask,
            'hero_stat': hero_stat,
        }

    def observation(self, obs):
        done = False
        action_queue = ''
        while not done:
            if action_queue:
                obs, reward, done, info = self.env.step(self.action2id.get(action_queue[0]))
                self.episode_reward += reward
                action_queue = action_queue[1:]
                continue

            action_queue = self.kernel.update(obs)
            if action_queue:
                continue

            # first-fit action selection
            level = self.kernel.curLevel()
            for name, action in self.kernel.personality.curBrain.actions.items():
                # check if an action can be taken
                can_act, mask = action.can(level)
                if not can_act:
                    action.after_search(mask, None)
                    continue

                if type(action) == RangeAttackMonster:
                    # return control to RL
                    return obs, done, True

                # local actions do not need pathfinding and return mask = None
                if mask is None:
                    action.execute()  # XXX path is None by default!
                    action.after_search(mask, None)
                    break

                # actions that potentially require navigaton
                path = dijkstra_cpp(level.tiles, self.kernel.hero.coords(), mask, level.tiles.is_opened_door)
                action.after_search(mask, path)
                if path is None:
                    continue

                # input(f'TYPE: {type(action)}')

                if type(action) == AttackMonster:
                    # return control to RL
                    return obs, done, False

                action.execute(path)
                break

            # input(f'actio_queue {action_queue}')
            action_queue = self.kernel.action

        return obs, done, False
