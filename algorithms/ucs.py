import heapq
from utils import get_neighbors

def ucs(initial_state, goal_state):
    queue = [(0, initial_state, [])]
    visited = set()

    while queue:
        cost, state, path = heapq.heappop(queue)
        if state == goal_state:
            return path + [state]
        visited.add(state)

        for neighbor in get_neighbors(state):
            if neighbor not in visited:
                heapq.heappush(queue, (cost + 1, neighbor, path + [neighbor]))

    return None
