import math
import torch
import torch.optim as optim
import random

from torch import nn, Tensor

from Monopolotron.Model.NN import NN
from Monopolotron.Model.replay_memory import ReplayMemory
import Monopolotron.Model.settings as settings


class DQNAgent():
    def __init__(self, eps=None):
        self.device = torch.device("cuda" if torch.cuda.is_available()
                                   else "cpu")
        self.policy_model = NN(settings.state_size).to(self.device)
        self.target_model = NN(settings.state_size).to(self.device)
        self.target_model.load_state_dict(self.policy_model.state_dict())

        self.memory = ReplayMemory()
        self.optim = optim.AdamW(self.policy_model.parameters(),
                                 lr=settings.learning_rate, amsgrad=True)
        self.criterion = nn.SmoothL1Loss()

        if not eps:
            self.epsilon = settings.epsilon_init
        else:
            self.epsilon = eps
        self.steps = 0

    def __update_epsilon(self):
        if self.epsilon > settings.epsilon_min:
            self.epsilon = self.epsilon * \
                           math.exp(-1. * self.steps * settings.epsilon_decay)

    def act(self, state) -> Tensor:
        self.__update_epsilon()
        self.steps += 1
        choice = random.random()
        if choice > self.epsilon:
            with torch.no_grad():
                out = self.policy_model(state.to(self.device))\
                        .max(0).indices.view(1)
                return out
        else:
            out = torch.tensor([random.randint(0, 1)], device=self.device)
            return out

    def replay(self):
        if len(self.memory) < settings.memory_size:
            return
        batch = self.memory.sample()
        batch = list(map(list, zip(*batch)))
        state_batch = torch.stack(batch[0])
        action_batch = torch.stack(batch[1])
        reward_batch = torch.stack(batch[2])
        next_state_batch = torch.stack(batch[3])
        done_batch = torch.stack(batch[4])

        state_action_values = self.policy_model(state_batch)\
            .gather(0, action_batch)

        with torch.no_grad():
            future_rewards = self.target_model(next_state_batch).max(1).values

        expected_Q = reward_batch + (settings.gamma * future_rewards
                                     * (1-done_batch))

        loss = self.criterion(state_action_values, expected_Q.unsqueeze(1))

        self.optim.zero_grad()
        loss.backward()

        self.optim.step()

    def update_target(self):
        for target_param, local_param in zip(self.target_model.parameters(),
                                             self.policy_model.parameters()):
            target_param.data.copy_(settings.tau * local_param.data
                                    + (1.0 - settings.tau) * target_param.data)
