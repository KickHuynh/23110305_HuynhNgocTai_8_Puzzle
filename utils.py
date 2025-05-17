def get_neighbors(state):
    # Kiểm tra state hợp lệ
    if not (isinstance(state, (list, tuple)) and len(state) == 3 and all(isinstance(row, (list, tuple)) and len(row) == 3 for row in state)):
        print('get_neighbors: state không hợp lệ:', state)
        return []
    neighbors = []
    rows, cols = 3, 3
    empty_pos = [(r, c) for r in range(rows) for c in range(cols) if state[r][c] == 0]
    if not empty_pos:
        print('get_neighbors: Không tìm thấy ô trống trong state:', state)
        return []
    empty_row, empty_col = empty_pos[0]

    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]  # Lên, Xuống, Trái, Phải
    for dr, dc in directions:
        new_row, new_col = empty_row + dr, empty_col + dc
        if 0 <= new_row < rows and 0 <= new_col < cols:
            new_state = [list(row) for row in state]
            new_state[empty_row][empty_col], new_state[new_row][new_col] = new_state[new_row][new_col], new_state[empty_row][empty_col]
            # Đảm bảo trả về tuple 3x3
            neighbors.append(tuple(tuple(row) for row in new_state))

    return neighbors

def heuristic(state, goal_state):
    return sum(1 for r in range(3) for c in range(3) if state[r][c] != goal_state[r][c] and state[r][c] != 0)

def manhattan_heuristic(state, goal_state):
    distance = 0
    for r in range(3):
        for c in range(3):
            value = state[r][c]
            if value != 0:
                gr, gc = divmod(value - 1, 3)
                distance += abs(r - gr) + abs(c - gc)
    return distance


def mismatch_heuristic(state, goal_state):
    return sum(1 for r in range(3) for c in range(3) if state[r][c] != goal_state[r][c] and state[r][c] != 0)
