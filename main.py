from Monopolotron.Model.DQNAgent import DQNAgent
from Monopolotron.Model.train_dqn import train_dqn
import numpy as np
import csv


if __name__ == "__main__":
    dqn = DQNAgent()
    epochs = 5000
    hist = train_dqn(dqn, epochs)
    chunks = epochs // 500
    for chunk in np.array_split(hist, chunks):
        print(f'Success number: {np.mean(chunk)}')

    with open('train_hist.csv', 'w') as f:
        write = csv.writer(f)
        write.writerow(hist)
