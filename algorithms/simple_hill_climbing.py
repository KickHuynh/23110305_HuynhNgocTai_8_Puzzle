from utils import get_neighbors, heuristic

def simple_hill_climbing(initial_state, goal_state):
    current_state = initial_state
    path = [current_state]

    while True:
        neighbors = get_neighbors(current_state)
        best_neighbor = None
        best_heuristic = heuristic(current_state, goal_state)

        for neighbor in neighbors:
            h = heuristic(neighbor, goal_state)
            if h < best_heuristic:
                best_neighbor = neighbor
                best_heuristic = h

        if best_neighbor is None:
            return path if current_state == goal_state else None

        current_state = best_neighbor
        path.append(current_state)
