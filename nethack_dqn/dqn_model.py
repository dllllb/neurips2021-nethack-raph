import torch
import torch.nn as nn
import numpy as np
import copy

EMBEDDING_DIM = 16


class DuelDQNModel(nn.Module):
    """A Dueling DQN net"""
    
    def __init__(self, input_shape, n_actions):
        super(DuelDQNModel, self).__init__()

        self.n_actions = n_actions

        self.embedding = nn.Embedding(256, EMBEDDING_DIM)

        self.conv = nn.Sequential(
            nn.Conv2d(EMBEDDING_DIM, 32, kernel_size=4, stride=2),
            nn.ReLU(),
            nn.Conv2d(32, 64, kernel_size=4, stride=2),
            nn.ReLU(),
            nn.Conv2d(64, 64, kernel_size=3, stride=1),
            nn.ReLU()
        )

        conv_out_size = self._get_conv_out(input_shape, self.conv)

        self.fc_adv = nn.Sequential(
            nn.Linear(conv_out_size, 512),
            nn.ReLU(),
            nn.Linear(512, 512),
            nn.ReLU(),
            nn.Linear(512, self.n_actions)
        )
        # h_adv = self.fc_adv.register_hook(lambda grad: grad/torch.sqrt(2))
        self.fc_val = nn.Sequential(
            nn.Linear(conv_out_size, 512),
            nn.ReLU(),
            nn.Linear(512, 512),
            nn.ReLU(),
            nn.Linear(512, 1)
        )
        # h_val = self.fc_val.register_hook(lambda grad: grad/torch.sqrt(2))

    def _get_conv_out(self, shape, conv):
        o = conv(torch.zeros(1, EMBEDDING_DIM, *shape))
        return int(np.prod(o.shape))

    def forward(self, x):
        x = self.embedding(x.long())
        x = x.permute(0, 3, 1, 2)

        conv_out = self.conv(x).view(x.shape[0], -1)

        val = self.fc_val(conv_out)
        adv = self.fc_adv(conv_out)

        return val + adv - adv.mean()


class TargetNet:
    """
    Wrapper around model which provides copy of it instead of trained weights
    """
    def __init__(self, model):
        self.model = model
        self.target_model = copy.deepcopy(model)

    def sync(self):
        self.target_model.load_state_dict(self.model.state_dict())


class DQNAgent:
    """
    Simple DQNAgent which calculates Q values from list of observations
                          calculates actions given np.array of qvalues
    """
    def __init__(self, dqn_model, epsilon, device):
        
        self.dqn_model = dqn_model
        self.epsilon = epsilon
        self.device = device

    def get_number_of_actions(self):
        return self.dqn_model.n_actions

    def get_q_values(self, states):
        """
        Calculates q-values given list of obseravations
        """
        
        states = self._state_processor(states)

        q_values = self.dqn_model.forward(states)

        return q_values.detach().cpu().numpy()

    def _state_processor(self, states):
        """
        Conversts list of states into torch tensor and copies it to the device
        """
        
        # return torch.tensor(states).to(self.device)
        return torch.from_numpy(np.array(states)).to(self.device)          

    def sample_actions(self, states, greedy=False):
        """
        Pick actions given array of qvalues
        Uses epsilon-greedy exploration strategy
        """
        
        qvalues = self.get_q_values(states)
        best_actions = qvalues.argmax(axis=-1)
        if greedy:
            return best_actions
        
        batch_size, n_actions = qvalues.shape
        
        mask = np.random.random(size=batch_size) < self.epsilon
        random_actions = np.random.choice(n_actions, size=sum(mask))        
        best_actions[mask] = random_actions
        
        return best_actions
