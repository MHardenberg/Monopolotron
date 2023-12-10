memory_size = 1000
epsilon_init = 1
epsilon_min = 0.01
epsilon_decay = 0.0001
gamma = 0.99
batch_size = 512
target_update = 5
learning_rate = 0.00001
state_size = 169
tau = 0.005
max_turns = 750


# Reward
reward_multipliers: dict = {
        'street': 2.,
        'house': 20.,
        'money': 1.,
        'victory': 1e6,
        'defeat': 0#-1e4
        }
