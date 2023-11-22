import random
from collections import namedtuple
from collections import deque
from Monopolotron.Model.settings import *

Transition = namedtuple('Transition', ('state', 'action', 'reward', 'next_state', 'done'))

class ReplayMemory:
    def __init__(self):
        self.memory = deque(maxlen=memory_size)

    def update(self, *args):
        self.memory.append(Transition(*args))

    def sample(self):
        return random.sample(self.memory, batch_size)

    def __len__(self):
        return len(self.memory)
