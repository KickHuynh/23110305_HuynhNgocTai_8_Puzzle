from collections import deque
from utils import get_neighbors

def bfs(initial_state, goal_state):
    queue = deque([(initial_state, [])])
    visited = set()

    while queue:
        state, path = queue.popleft()
        if state == goal_state:
            return path + [state]
        visited.add(state)

        for neighbor in get_neighbors(state):
            if neighbor not in visited:
                queue.append((neighbor, path + [neighbor]))

    return None
