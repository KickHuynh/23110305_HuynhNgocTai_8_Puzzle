import random
import math
from utils import get_neighbors, heuristic

def simulated_annealing(initial_state, goal_state, initial_temp=1000.0, cooling_rate=0.99, min_temp=0.01, max_no_improvement=2000, max_steps=10000):
    current = initial_state
    path = [current]
    explored_states = set()
    current_heuristic = heuristic(current, goal_state)

    temperature = initial_temp
    no_improvement_count = 0
    steps = 0

    while temperature > min_temp and no_improvement_count < max_no_improvement and steps < max_steps:
        explored_states.add(current)
        neighbors = get_neighbors(current)
        if not neighbors:
            break

        neighbor_heuristic_pairs = [(neighbor, heuristic(neighbor, goal_state)) for neighbor in neighbors]
        neighbor_heuristic_pairs.sort(key=lambda x: x[1])
        next_state, next_heuristic = neighbor_heuristic_pairs[0]

        if next_heuristic >= current_heuristic:
            delta = next_heuristic - current_heuristic
            acceptance_probability = math.exp(-delta / temperature)
            if random.uniform(0, 1) > acceptance_probability:
                next_state, next_heuristic = random.choice(neighbor_heuristic_pairs)

        if next_heuristic < current_heuristic:
            no_improvement_count = 0
        else:
            no_improvement_count += 1

        current = next_state
        current_heuristic = next_heuristic
        path.append(current)

        if current == goal_state:
            return path, list(explored_states)

        temperature *= cooling_rate
        steps += 1

    # Không tìm được lời giải, trả về None
    return None, list(explored_states)