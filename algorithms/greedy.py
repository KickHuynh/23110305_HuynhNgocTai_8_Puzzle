import heapq
from utils import get_neighbors, heuristic

def greedy(initial_state, goal_state):
    queue = [(heuristic(initial_state, goal_state), initial_state, [])]
    visited = set()

    while queue:
        _, state, path = heapq.heappop(queue)
        if state == goal_state:
            return path + [state]

        visited.add(state)

        for neighbor in get_neighbors(state):
            if neighbor not in visited:
                heapq.heappush(queue, (heuristic(neighbor, goal_state), neighbor, path + [neighbor]))

    return None
