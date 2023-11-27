import math
import torch
import torch.optim as optim
import random

from torch import nn

from Monopolotron.Model.NN import NN
from Monopolotron.Model.replay_memory import ReplayMemory
import Monopolotron.Model.settings as settings


class DQNAgent():
    def __init__(self, model_state_dict: dict, players_cont: int):
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        self.model = DQNAgent()
        if model_state_dict:
            self.model.load_state_dict(model_state_dict)
        
        self.model.to(self.device)
        self.model.eval()

        # setup policy and target model
        self.policy_model = NN(settings.state_size)
        self.target_model = NN(settings.state_size)
        self.target_model.load_state_dict(self.policy_model.state_dict())
        # Initialize target model with policy model's weight

        self.target_update_counter = 0
        # target model updated every x target_update steps,
        # used to calculate Q-values, so it's more stable

        self.player_memory = [ReplayMemory() for _ in range(players_cont)]
        self.optim = optim.AdamW(self.policy_model.parameters(),
                                 lr=settings.learning_rate, amsgrad=True)
        self.epsilon = settings.epsilon_init
        self.steps = 0

        # init game state 
        self.player_game_state = [torch.zeros(model_settings.state_size) \
                for _ in range(players_cont)

        for i, _ in enumerate(self.player_game_state):
            self.player_game_state[i].to(self.device)

    def __update_epsilon(self):
        if self.epsilon > settings.epsilon_min:
            self.epsilon = self.epsilon * \
                math.exp(-1. * self.steps * settings.epsilon_decay)

    def act(self, state:torch.Tensor, player_idx: int) -> int:
        """ This function only takes decisions. It is supposed to be called 
        seperately from the .learn() method, when a decision has to be taken.
        This seperation has been done,
        as the full state (incl. done) is only known after all actors 
        finish their turn.
        """
        self.player_game_state[player_idx] = state
        self.model.eval()

        choice = random.random()
        if choice > self.epsilon:
            with torch.no_grad():
                return self.policy_model(state).max(1).indices
        return random.randint(0, 1)  # may need ot be changed

    def replay(player_idx: int, self, action: int, done: bool) -> None:
        """ This function takes care of learning after action was taken. It is 
        supposed to be called at the end of a full round.
        """
        state = self.player_game_state[player_idx]
        reward = self.__eval_reward(state)
        self.__store_experience(player_idx, state, action, reward, done)

        self.__update_epsilon()
        self.steps += 1

    def __update_model():
        print("Warning not implemented")
        pass

    def __eval_reward(state) -> float:
        assert False,  AssertionError('Not implemented')

    def __store_experience(self, player_idx: int, state, action,
                           reward, next_state, done):
        self.player_memory[player_idx]\
                .push(state, action, reward, next_state, done)

        # Call replay periodically
        if self.steps % settings.replay_frequency == 0:
            self.__replay(player_idx)

    def __replay(self, player_idx: int):
        if len(self.player_memory[player_idx]) < settings.batch_size:
            return

        self.model.train()

        batch = self.player_memory[player_idx].sample()
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
