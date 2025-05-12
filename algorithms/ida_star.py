from utils import get_neighbors, heuristic

def ida_star(initial_state, goal_state):
    bound = heuristic(initial_state, goal_state)
    path = [initial_state]

    def search(path, g, bound):
        state = path[-1]
        f = g + heuristic(state, goal_state)
        if f > bound:
            return f
        if state == goal_state:
            return path
        min_bound = float('inf')

        for neighbor in get_neighbors(state):
            if neighbor not in path:
                result = search(path + [neighbor], g + 1, bound)
                if isinstance(result, list):
                    return result
                min_bound = min(min_bound, result)

        return min_bound

    while True:
        result = search(path, 0, bound)
        if isinstance(result, list):
            return result
        if result == float('inf'):
            return None
        bound = result
