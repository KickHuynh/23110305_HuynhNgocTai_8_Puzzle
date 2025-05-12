import heapq
from utils import get_neighbors, heuristic

def a_star(initial_state, goal_state):
    queue = [(heuristic(initial_state, goal_state), 0, initial_state, [])]
    visited = set()

    while queue:
        _, cost, state, path = heapq.heappop(queue)
        if state == goal_state:
            return path + [state]

        visited.add(state)

        for neighbor in get_neighbors(state):
            if neighbor not in visited:
                total_cost = cost + 1
                heapq.heappush(queue, (total_cost + heuristic(neighbor, goal_state), total_cost, neighbor, path + [neighbor]))

    return None
