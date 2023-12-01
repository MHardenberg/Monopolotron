memory_size = 2000
epochs = 200
epsilon_init = 1
epsilon_min = 0.1
epsilon_decay = 0.0001
gamma = 0.9
batch_size = 256
target_update = 10
learning_rate = 0.0001
state_size = 169
tau = 0.005
max_turns = 500


# Reward
reward_multipliers: dict = {
        'street': 1.1,
        'house': 1.2,
        'money': 1.
        }
