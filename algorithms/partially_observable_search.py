from utils import get_neighbors

def is_goal_belief(belief_states, goal_state):
    return all(state == goal_state for state in belief_states)

def partially_observable_search(initial_belief_states, goal_state):
    from collections import deque

    visited = set()
    queue = deque()
    queue.append((tuple(initial_belief_states), []))

    while queue:
        current_belief, path = queue.popleft()
        if is_goal_belief(current_belief, goal_state):
            return path + [current_belief]
        if current_belief in visited:
            continue
        visited.add(current_belief)

        # Sinh các belief state tiếp theo bằng cách áp dụng mọi hành động cho từng trạng thái
        next_beliefs = []
        for i, state in enumerate(current_belief):
            neighbors = get_neighbors(state)
            for neighbor in neighbors:
                new_belief = list(current_belief)
                new_belief[i] = neighbor
                next_beliefs.append(tuple(new_belief))

        for next_belief in next_beliefs:
            if next_belief not in visited:
                queue.append((next_belief, path + [current_belief]))

    return None