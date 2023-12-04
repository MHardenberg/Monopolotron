from Monopolotron.Model.DQNAgent import DQNAgent
from Monopolotron.Model.train_dqn import train_dqn
import numpy as np


if __name__ == "__main__":
    dqn = DQNAgent()
    hist = train_dqn(dqn, 1000)
    chunks = 10
    for chunk in np.array_split(hist, chunks):
        print(f'Success number: {np.mean(chunk)}')
