from agents.base import BatchedAgent
from nethack_raph.Kernel import Kernel

from nle.nethack.actions import ACTIONS
import time

import multiprocessing as mp


class Agent:
    def __init__(self):
        super().__init__()

        self.action2id = {
            chr(action.value): action_id for action_id, action in enumerate(ACTIONS)
        }

        self.kernel = Kernel(silent=True)

    def reset(self):
        del self.kernel
        self.kernel = Kernel(silent=True)

    def step(self, obs):
        action = self.kernel.step(obs)
        if len(action):
            ch = action[0]
        else:
            #TODO check if it happens
            ch = ' '

        action = self.action2id.get(ch)
        if action is None:
            #TODO check if it happens
            action = 0
        return action


class Process(mp.Process):
    def __init__(self, remote, parent_remote, daemon=True):
        super().__init__(daemon=daemon)
        self.remote = remote
        self.parent_remote = parent_remote
        self.agent = None#Agent()

    def run(self):
        if self.agent is None:
            self.agent = Agent()
        self.parent_remote.close()
        while True:
            try:
                observation, done = self.remote.recv()
                if done:
                    self.agent.reset()
                action = self.agent.step(observation)
                self.remote.send(action)
            except EOFError:
                break


class SubprocVecEnv:
    def __init__(self, n_processes):
        self.waiting = False

        # Fork is not a thread safe method (see issue #217)
        # but is more user friendly (does not require to wrap the code in
        # a `if __name__ == "__main__":`)
        forkserver_available = "forkserver" in mp.get_all_start_methods()
        start_method = "forkserver" if forkserver_available else "spawn"
        ctx = mp.get_context(start_method)

        self.remotes, self.work_remotes = zip(*[ctx.Pipe() for _ in range(n_processes)])
        self.processes = []
        for work_remote, remote in zip(self.work_remotes, self.remotes):
            # daemon=True: if the main process crashes, we should not cause things to hang
            process = Process(work_remote, remote, daemon=True)  # pytype:disable=attribute-error
            process.start()
            self.processes.append(process)
            work_remote.close()

    def step(self, states, dones):
        self.step_async(states, dones)
        return self.step_wait()

    def step_async(self, states, dones):
        for remote, state, done in zip(self.remotes, states, dones):
            remote.send((state, done))
        self.waiting = True

    def step_wait(self):
        results = [remote.recv() for remote in self.remotes]
        self.waiting = False
        return results


class CustomAgentMP(BatchedAgent):
    def __init__(self, num_envs, num_actions):
        """Set up and load you model here"""
        super().__init__(num_envs, num_actions)
        self.agents = SubprocVecEnv(num_envs)

    def batched_step(self, observations, rewards, dones, infos):
        """
        Perform a batched step on lists of environment outputs.

        Each argument is a list of the respective gym output.
        Returns an iterable of actions.
        """
        return self.agents.step(observations, dones)


class CustomAgent(BatchedAgent):
    """A example agent... that simple acts randomly. Adapt to your needs!"""

    def __init__(self, num_envs, num_actions):
        """Set up and load you model here"""
        super().__init__(num_envs, num_actions)
        self.kernel = Kernel(silent=False)

        self.action2id = {
            chr(action.value): action_id for action_id, action in enumerate(ACTIONS)
        }

        self.maxtime = 0
        self.reward = 0

    def batched_step(self, observations, rewards, dones, infos):
        """
        Perform a batched step on lists of environment outputs.

        Each argument is a list of the respective gym output.
        Returns an iterable of actions.
        """

        assert len(dones) == 1
        self.reward += rewards[0]


        if int(dones[0]):
            input(f'tot reward: {self.reward}')
            del self.kernel
            self.kernel = Kernel(silent=False)
            self.reward = 0


        before = time.time()

        action = self.kernel.step(observations[0])
        if len(action):
            ch = action[0]
        else:
            #TODO check if it happens
            ch = ' '

        action = self.action2id.get(ch)
        if action is None:
            #TODO check if it happens
            action = 0

        after = time.time()
        self.maxtime = max(self.maxtime, after - before)

        self.kernel.log("Sent string:" + ch + ' ' + str(type(ch)))
        self.kernel.log("Sent string:" + ch + ' ' + str(action))
        self.kernel.log(f'action time: {after - before}, maxtime: {self.maxtime}')
        return [action]
