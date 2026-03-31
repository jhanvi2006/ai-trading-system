import random

class TradingAgent:

    def __init__(self, state_size, action_size, lr, gamma, epsilon):
        self.lr = lr
        self.gamma = gamma
        self.epsilon = epsilon
        self.q_table = {}

    def get_q(self, state):
        return self.q_table.get(tuple(state), [0, 0, 0])

    def choose_action(self, state):

        if random.random() < self.epsilon:
            return random.randint(0, 2)

        return self.get_q(state).index(max(self.get_q(state)))

    def update(self, state, action, reward, next_state):

        q = self.get_q(state)
        next_q = self.get_q(next_state)

        q[action] += self.lr * (reward + self.gamma * max(next_q) - q[action])

        self.q_table[tuple(state)] = q