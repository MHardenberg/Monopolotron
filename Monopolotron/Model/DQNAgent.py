import math
import torch
import torch.optim as optim
import random

from torch import nn

from Monopolotron.Model.NN import NN
from Monopolotron.Model.replay_memory import ReplayMemory
import Monopolotron.Model.settings as settings


class DQNAgent():
    def __init__(self):
        self.policy_model = NN(settings.state_size)
        self.target_model = NN(settings.state_size)
        self.target_model.load_state_dict(self.policy_model.state_dict())
        # Initialize target model with policy model's weights
        self.target_update_counter = 0
        # target model updated every x target_update steps,
        # used to calculate Q-values, so it's more stable

        self.memory = ReplayMemory()
        self.optim = optim.AdamW(self.policy_model.parameters(),
                                 lr=settings.learning_rate, amsgrad=True)
        self.epsilon = settings.epsilon_init
        self.steps = 0

    def __update_epsilon(self):
        if self.epsilon > settings.epsilon_min:
            self.epsilon = self.epsilon * \
                math.exp(-1. * self.steps * settings.epsilon_decay)

    def act(self, state:torch.Tensor, done: bool) -> int:
        self.__update_epsilon()
        self.steps += 1
        choice = random.random()
        if choice > self.epsilon:
            with torch.no_grad():
                action = self.policy_model(state).max(1).indices
        else:
            action = random.randint(0, 1)  # may need ot be changed

        reward = self.__eval_reward(state)
        self.__store_experience(state, action, reward, done)
        return action

    def __eval_reward(state) -> float:
        assert False,  AssertionError('Not implemented')

    def __store_experience(self, state, action, reward, next_state, done):
        self.memory.push(state, action, reward, next_state, done)

        # Call replay periodically
        if self.steps % settings.replay_frequency == 0:
            self.__replay()

    def __replay(self):
        if len(self.memory) < settings.batch_size:
            return

        batch = self.memory.sample()
        # can change to do whole batch at once later on
        for state, action, reward, next_state, done in batch:
            state_action_values = []
            if not done:
                state_action_values = self.policy_model(state).max(1).value

            with torch.no_grad():
                next_state_values = self.target_model(next_state).max(1).values

            target = reward + settings.gamma * next_state_values
            criterion = nn.SmoothL1Loss()

            loss = criterion(state_action_values, target)
            self.optim.zero_grad()
            loss.backward()
            torch.nn.utils.clip_grad_value_(self.policy_model.parameters(),
                                            100)
            self.optim.step()

            # Update target network every C steps
            self.target_update_counter += 1
            if self.target_update_counter % settings.target_update_freq == 0:
                self.target_model.load_state_dict(
                        self.policy_model.state_dict())
