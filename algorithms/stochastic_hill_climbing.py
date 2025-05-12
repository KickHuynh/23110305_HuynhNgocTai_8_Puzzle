import random
from utils import get_neighbors, heuristic

def stochastic_hill_climbing(initial_state, goal_state):
    current_state = initial_state
    path = [current_state]

    while True:
        neighbors = get_neighbors(current_state)
        if not neighbors:
            return path if current_state == goal_state else None

        better_neighbors = [n for n in neighbors if heuristic(n, goal_state) < heuristic(current_state, goal_state)]
        if not better_neighbors:
            return path if current_state == goal_state else None

        current_state = random.choice(better_neighbors)
        path.append(current_state)
