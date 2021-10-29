from nethack_raph.Actions.base import BaseAction
from nethack_raph.Actions.LaunchAttack import LaunchAttack
from nethack_raph.Actions.ThrowAttack import ThrowAttack


class RangeAttack(BaseAction):
    def __init__(self, kernel):
        self.throw_action = ThrowAttack(kernel)
        self.launch_action = LaunchAttack(kernel)
        self.action_to_do = None
        self.exp_damage = 0
        super().__init__(kernel)

    def can(self, level):
        can_throw, _ = self.throw_action.can(level)
        can_launch, _ = self.launch_action.can(level)

        if not can_throw and not can_launch:
            return False, None
        elif can_throw and not can_launch:
            self.exp_damage = self.throw_action.exp_damage
            self.action_to_do = 'throw'
            return True, None
        elif not can_throw and can_launch:
            self.exp_damage = self.launch_action.exp_damage
            self.action_to_do = 'launch'
            return True, None
        else:
            if self.throw_action.exp_damage >= self.launch_action.exp_damage:
                self.exp_damage = self.throw_action.exp_damage
                self.action_to_do = 'throw'
            else:
                self.exp_damage = self.launch_action.exp_damage
                self.action_to_do = 'launch'
            return True, None

    def execute(self, path=None):
        if self.action_to_do == 'throw':
            self.throw_action.execute(path)
        else:
            self.launch_action.execute(path)
