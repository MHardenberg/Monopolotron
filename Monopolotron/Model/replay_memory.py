import random
from collections import namedtuple
from collections import deque

import torch

from Monopolotron.Model.settings import *

class ReplayMemory:
    def __init__(self):
        self.memory = deque(maxlen=memory_size)

    def update(self, state, action, reward, next_state, done):
        self.memory.append([state, action, reward, next_state, done])

    def done(self):
        self.memory[-1][-1] = torch.tensor(1, device=torch.device("cuda" if torch.cuda.is_available() else "cpu"))

    def sample(self):
        return random.sample(self.memory, batch_size)

    def __len__(self):
        return len(self.memory)
