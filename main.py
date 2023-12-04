from Monopolotron.Model.DQNAgent import DQNAgent
from Monopolotron.Model.train_dqn import train_dqn
import numpy as np


if __name__ == "__main__":
    dqn = DQNAgent()
    hist = train_dqn(dqn, 1000)
    chunk_size = 10
    for chunk in np.array_split(hist, chunk_size):
        print(f'Success number: {np.mean(chunk)}')

