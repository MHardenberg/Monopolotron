from Monopolotron.Model.DQNAgent import DQNAgent
from Monopolotron.Model.train_dqn import train_dqn
import numpy as np
import csv
import torch


if __name__ == "__main__":
    dqn = DQNAgent()
    epochs = 1000
    print(f'Running training for {epochs} epochs...')
    hist = train_dqn(dqn, epochs)
    chunks = epochs // 50
    for chunk in np.array_split(hist, chunks):
        print(f'Success number: {np.mean(chunk)}')

    with open('train_hist.csv', 'w') as f:
        write = csv.writer(f)
        write.writerow(hist)

    torch.save(dqn.state_dict(), 'model_state.pt')
