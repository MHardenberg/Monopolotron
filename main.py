from Monopolotron.Model.DQNAgent import DQNAgent
from Monopolotron.Model.train_dqn import train_dqn
import numpy as np
import csv
import torch


if __name__ == "__main__":
    try:
        with open('model_weights/last_eps.csv', 'r') as f:
            reader = csv.reader(f)
            eps = float(next(reader)[0])
            print(f'Using current eps: {eps}')
    except FileNotFoundError:
        print('No last_eps.csv found. Using starting settings...')
        eps = None

    dqn = DQNAgent(eps=eps)
    epochs = 2000

    try:
        dqn.policy_model.load_state_dict(
                torch.load('model_weights/p_model_state.pt'))
        dqn.target_model.load_state_dict(
                torch.load('model_weights/t_model_state.pt'))

    except FileNotFoundError:
        print('No model state found - creating new ..')

    print(f'Running training for {epochs} epochs...')
    hist = train_dqn(dqn, epochs)
    eps = dqn.epsilon
    chunks = epochs // 10
    for chunk in np.array_split(hist, chunks):
        print(f'Success number: {np.mean(chunk)}')

    with open('stats/train_hist.csv', 'a') as f:
        write = csv.writer(f)
        write.writerow(hist)

    with open('model_weights/last_eps.csv', 'w') as f:
        write = csv.writer(f)
        write.writerow((eps,))

    torch.save(dqn.policy_model.state_dict(), 'model_weights/p_model_state.pt')
    torch.save(dqn.target_model.state_dict(), 'model_weights/t_model_state.pt')
