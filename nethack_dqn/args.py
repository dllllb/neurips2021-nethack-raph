import argparse
import torch


def get_args(flag=None):
    parser = argparse.ArgumentParser()

    group = parser.add_argument_group('system parameters')
    group.add_argument(
        '--cuda', type=int, default=0, help='ID of GPU to use, -1 for disabled')

    group = parser.add_argument_group('DQN parameters')
    group.add_argument('--total-steps',type=int,default=int(1e8),
                        help='Total number of learning steps')
    group.add_argument('--decay-steps',type=int,default=int(1e6),
                        help='Number of learning steps for epsilon decay')
    group.add_argument('--rollout-steps',type=int,default=4,
                        help='Number of learning steps for epsilon decay')                 
    group.add_argument('--init-eps',type=float,default=1,
                        help='Initial epsilon value')
    group.add_argument('--final-eps',type=float,default=0.1,
                        help='Final epsilon value')
    group.add_argument('--eval-eps',type=float,default=0.05,
                        help='Final epsilon value')
    group.add_argument('--loss-freq',type=int,default=10000,
                        help='Number of steps between loss traking')
    group.add_argument('--target-net-freq',type=int,default=10000,
                        help='Nuber of steps between target network updates')
    group.add_argument('--eval-freq',type=int,default=100000,
                        help='Nuber of steps between evaluations')
    group.add_argument('--plot-freq',type=int,default=100000,
                        help='Nuber of steps between evaluations')
    group.add_argument('--grad-norm',type=int,default=50,
                        help='Max gradients norm')
    group.add_argument('--batch-size',type=int,default=32,
                        help='Training batch size')
    group.add_argument('--buffer-size',type=int,default=int(1e6),
                        help='Replay buffer size')
    group.add_argument('--init-buff-size',type=int,default=int(5e4),
                        help='Initial replay buffer population')
    group.add_argument('--lr',type=float,default=2.5e-4,
                        help='Learning rate')
    group.add_argument('--gamma',type=float,default=.99,
                        help='DQN discount factor')
    group.add_argument('--loss-type',type=str,default='Huber',choices=['MSE','Huber'],
                        help='DQN loss type')
    group.add_argument('--double',action='store_true',default=False,
                        help='Double DQN')
    group.add_argument('--duel',action='store_true',default=False,
                        help='Dueling DQN')
    group.add_argument('--plot-show',action='store_true',default=False,
                        help='Option show plots or save')

    group = parser.add_argument_group('Atari environment parameters')
    group.add_argument('--env-name',type=str,default='PongNoFrameskip-v4',
                        help='Atari env name')
    group.add_argument('--episode-life',action='store_true',default=True,
                        help='Make end-of-life == end-of-episode, but only reset on true game over')
    group.add_argument('--clip-rewards',action='store_true',default=True,
                        help='Clip rewards to +-1')
    group.add_argument('--frame-stack',type=int,default=4,
                        help='Number of frames in frame-stack')
    group.add_argument('--frame-skip',type=int,default=4,
                        help='Number of skipped frames between observations')
    group.add_argument('--torch-idx',action='store_true',default=True,
                        help='Use torch-type indexing for batches')
    group.add_argument('--scale',action='store_true',default=False,
                        help='Scales frames')

    if flag=='nb':
        args = parser.parse_args(args=[])
    else:
        args = parser.parse_args()

    if torch.cuda.is_available():
            args.device = torch.device('cuda', vars(args)['cuda'])
    else:
        args.device = torch.device('cpu')
    
    return args