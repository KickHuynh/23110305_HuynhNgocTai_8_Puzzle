import random
import pickle
from utils import get_neighbors

class QLearningAgent:
    def __init__(self, alpha=0.1, gamma=0.9, epsilon=0.2):
        self.q_table = {}
        self.alpha = alpha      # learning rate
        self.gamma = gamma      # discount factor
        self.epsilon = epsilon  # exploration rate

    def get_q(self, state, action):
        return self.q_table.get((state, action), 0.0)

    def choose_action(self, state):
        neighbors = get_neighbors(state)
        if random.random() < self.epsilon:
            return random.choice(neighbors)
        qs = [self.get_q(state, a) for a in neighbors]
        max_q = max(qs)
        best_actions = [a for a, q in zip(neighbors, qs) if q == max_q]
        return random.choice(best_actions)

    def learn(self, state, action, reward, next_state, done):
        prev_q = self.get_q(state, action)
        next_neighbors = get_neighbors(next_state)
        next_q = max([self.get_q(next_state, a) for a in next_neighbors], default=0)
        target = reward + (0 if done else self.gamma * next_q)
        self.q_table[(state, action)] = prev_q + self.alpha * (target - prev_q)

    def save(self, filename):
        with open(filename, 'wb') as f:
            pickle.dump(self.q_table, f)

    def load(self, filename):
        with open(filename, 'rb') as f:
            self.q_table = pickle.load(f)

def q_learning_train(initial_state, goal_state, episodes=10000, max_steps=100):
    agent = QLearningAgent()
    for ep in range(episodes):
        state = initial_state
        for step in range(max_steps):
            action = agent.choose_action(state)
            done = action == goal_state
            reward = 1 if done else -0.1
            agent.learn(state, action, reward, action, done)
            state = action
            if done:
                break
    agent.save("q_table.pkl")
    return agent

def q_learning_solve(initial_state, goal_state):
    agent = QLearningAgent()
    agent.load("q_table.pkl")
    state = initial_state
    path = [state]
    for _ in range(100):
        action = agent.choose_action(state)
        path.append(action)
        if action == goal_state:
            return path
        state = action
    return None
