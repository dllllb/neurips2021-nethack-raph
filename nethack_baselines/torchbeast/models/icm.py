import torch
from torch import nn
from torch.nn import functional as F
from .baseline import GlyphEncoder, MessageEncoder, BLStatsEncoder, NUM_FEATURES


def init(module, weight_init, bias_init, gain=1):
    weight_init(module.weight.data, gain=gain)
    bias_init(module.bias.data)
    return module


class StateEmbeddingNet(nn.Module):
    def __init__(self, observation_shape, action_space, flags, device):
        super(StateEmbeddingNet, self).__init__()

        self.flags = flags

        self.observation_shape = observation_shape
        self.num_actions = len(action_space)

        self.H = observation_shape[0]
        self.W = observation_shape[1]

        self.use_lstm = flags.use_lstm
        self.h_dim = flags.hidden_dim

        # GLYPH + CROP MODEL
        self.glyph_model = GlyphEncoder(flags, self.H, self.W, flags.crop_dim, device)

        # MESSAGING MODEL
        self.msg_model = MessageEncoder(
            flags.msg.hidden_dim, flags.msg.embedding_dim, device
        )

        # BLSTATS MODEL
        self.blstats_model = BLStatsEncoder(NUM_FEATURES, flags.embedding_dim)

        out_dim = (
            self.blstats_model.hidden_dim
            + self.glyph_model.hidden_dim
            + self.msg_model.hidden_dim
        )

        self.fc = nn.Sequential(
            nn.Linear(out_dim, self.output_dim()),
            nn.ReLU(),
        )

    def output_dim(self):
        return 256

    def forward(self, inputs):
        T, B, H, W = inputs["glyphs"].shape
        reps = []

        # -- [B' x K] ; B' == (T x B)
        glyphs_rep = self.glyph_model(inputs)
        reps.append(glyphs_rep)

        # -- [B' x K]
        char_rep = self.msg_model(inputs)
        reps.append(char_rep)

        # -- [B' x K]
        features_emb = self.blstats_model(inputs)
        reps.append(features_emb)

        # -- [B' x K]
        st = torch.cat(reps, dim=1)
        st = self.fc(st)
        return st.view(T, B, -1)


class InverseDynamicsNet(nn.Module):
    def __init__(self, num_actions, emb_size):
        super(InverseDynamicsNet, self).__init__()
        self.num_actions = num_actions

        init_ = lambda m: init(m, nn.init.orthogonal_, lambda x: nn.init.
                               constant_(x, 0), nn.init.calculate_gain('relu'))
        self.inverse_dynamics = nn.Sequential(
            init_(nn.Linear(2 * emb_size, 256)),
            nn.ReLU(),
        )

        init_ = lambda m: init(m, nn.init.orthogonal_,
                               lambda x: nn.init.constant_(x, 0))
        self.id_out = init_(nn.Linear(256, self.num_actions))

    def forward(self, state_embedding, next_state_embedding):
        inputs = torch.cat((state_embedding, next_state_embedding), dim=2)
        action_logits = self.id_out(self.inverse_dynamics(inputs))
        return action_logits


class ForwardDynamicsNet(nn.Module):
    def __init__(self, num_actions, emb_size):
        super(ForwardDynamicsNet, self).__init__()
        self.num_actions = num_actions

        init_ = lambda m: init(m, nn.init.orthogonal_, lambda x: nn.init.
                               constant_(x, 0), nn.init.calculate_gain('relu'))

        self.forward_dynamics = nn.Sequential(
            init_(nn.Linear(emb_size + self.num_actions, 256)),
            nn.ReLU(),
        )

        init_ = lambda m: init(m, nn.init.orthogonal_,
                               lambda x: nn.init.constant_(x, 0))

        self.fd_out = init_(nn.Linear(256, emb_size))

    def forward(self, state_embedding, action):
        action_one_hot = F.one_hot(action, num_classes=self.num_actions).float()
        inputs = torch.cat((state_embedding, action_one_hot), dim=2)
        next_state_emb = self.fd_out(self.forward_dynamics(inputs))
        return next_state_emb
