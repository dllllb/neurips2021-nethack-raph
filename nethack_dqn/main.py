from dqn_model import DuelDQNModel, DQNAgent, TargetNet
from replay_buffer import ReplayBuffer, fill
from common_utils import *
from nethack_wrapper import make_env
from args import get_args

import torch
import torch.nn as nn
from tqdm import trange
from tensorboardX import SummaryWriter

import os
import sys
PACKAGE_PARENT = '..'
SCRIPT_DIR = os.path.dirname(os.path.realpath(os.path.join(os.getcwd(), os.path.expanduser(__file__))))
sys.path.append(os.path.normpath(os.path.join(SCRIPT_DIR, PACKAGE_PARENT)))

from test_submission import evaluate


def main():
    writer = SummaryWriter('logs/simple')

    args = get_args()
    print(vars(args))

    env = make_env()
    print(env.action_space)
    observation_shape = env.observation_space.shape
    print('obs shape', observation_shape)
    n_actions = env.action_space.n
    net = DuelDQNModel(observation_shape, n_actions).to(args.device)

    target_net = TargetNet(net)
    exp_replay = ReplayBuffer(args.buffer_size)

    agent = DQNAgent(net, args.init_eps, args.device)
    if args.loss_type == 'MSE':
        loss = nn.MSELoss()
    elif args.loss_type == 'Huber':
        loss = nn.SmoothL1Loss()

    optimizer = torch.optim.Adam(net.parameters(), lr=args.lr)

    state = env.reset()
    state = fill(exp_replay, agent, env, state, n_steps=args.init_buff_size)

    step_begin = 0
    for step in trange(step_begin, step_begin + int(args.total_steps/args.rollout_steps + 1)):

        agent.epsilon = linear_decay(step, args)

        # play
        state = fill(exp_replay, agent, env, state, n_steps=args.rollout_steps)

        # train
        optimizer.zero_grad()
        batch = exp_replay.sample(args.rollout_steps * args.batch_size)

        loss_v = calc_loss_dqn(batch, net=net, tgt_net=target_net.target_model, args=args, loss=loss)
        loss_v.backward()

        if args.duel:
            duel_dqn_conv_grads_div(net)
        grad_norm = nn.utils.clip_grad_norm_(net.parameters(), args.grad_norm)
        optimizer.step()

        writer.add_scalar('loss', loss_v.item(), step)
        writer.add_scalar('grad_norm', grad_norm, step)

        if step % args.target_net_freq == 0:
            # Load agent weights into target_network
            target_net.sync()

        if step % args.eval_freq == 0:
            agent.epsilon = args.eval_eps

            with open('/Users/sodi/dev/sber/neurips-2021-the-nethack-challenge/saved_models/dqn/model', 'wb') as out:
                torch.save(net.state_dict(), out)
            print('evaluate')
            reward = evaluate()

            writer.add_scalar('reward', reward, step)

            agent.epsilon = linear_decay(step, args)
            
            print("Updates: {}, num timesteps: {}, buff size: {}, epsilon: {:.4f}, reward {:.2f}".format(
                step, int(step * args.rollout_steps), len(exp_replay), agent.epsilon, reward)
            )

        if step % 100000 == 0:
            torch.save(net.state_dict(), 'model_{}'.format(step))


if __name__ == '__main__':
    main()
