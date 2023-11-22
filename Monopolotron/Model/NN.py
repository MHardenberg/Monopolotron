import torch.nn as nn
import torch.nn.functional as F


class NN(nn.Module):
    ''' Some basic NN, to be modified later.
    '''

    def __init__(self, n_observations):
        super(NN, self).__init__()
        self.layer1 = nn.Linear(n_observations, 128)
        self.layer2 = nn.Linear(128, 128)
        self.layer3 = nn.Linear(128, 2)

    def forward(self, x):
        x = F.relu(self.layer1(x))
        x = F.relu(self.layer2(x))
        x = self.layer3(x)
        return x
