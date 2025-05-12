from utils import get_neighbors

def dfs(state, goal_state, visited=None, path=None, depth=0, max_depth=50):
    if visited is None:
        visited = set()
    if path is None:
        path = []

    if state == goal_state:
        return path + [state]

    if depth >= max_depth:
        return None

    visited.add(state)

    for neighbor in get_neighbors(state):
        if neighbor not in visited:
            result = dfs(neighbor, goal_state, visited, path + [neighbor], depth + 1, max_depth)
            if result is not None:
                return result

    return None
