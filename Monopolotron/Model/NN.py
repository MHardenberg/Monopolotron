import torch.nn as nn
import torch.nn.functional as F


class NN(nn.Module):
    ''' Some basic NN, to be modified later.
    '''

    def __init__(self, state_size):
        super(NN, self).__init__()
        self.layer1 = nn.Linear(state_size, 256)
        self.layer2 = nn.Linear(256, 256)
        self.layer3 = nn.Linear(256, 256)
        self.layer_out = nn.Linear(256, 2)

    def forward(self, x):
        x = F.relu(self.layer1(x))
        x = F.relu(self.layer2(x))
        x = F.relu(self.layer3(x))
        x = self.layer_out(x)
        return x
        x = F.relu(self.layer2(x))
