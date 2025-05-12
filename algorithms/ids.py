from utils import get_neighbors

def dfs(state, goal_state, path, depth, visited):
    """
    Perform DFS with depth limit.
    """
    if state == goal_state:
        return path + [state]
    if depth == 0:
        return None

    visited.add(state)

    for neighbor in get_neighbors(state):
        if neighbor not in visited:
            result = dfs(neighbor, goal_state, path + [neighbor], depth - 1, visited)
            if result:
                return result

    visited.remove(state)
    return None

def ids(initial_state, goal_state, max_depth=20):
    """
    Perform Iterative Deepening Search (IDS).
    """
    for depth in range(max_depth):
        visited = set()
        result = dfs(initial_state, goal_state, [], depth, visited)
        if result:
            return result
    return None
