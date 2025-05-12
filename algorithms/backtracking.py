# Đảm bảo có hàm backtracking
def backtracking(state, goal_state, depth_limit=30):
    # Giả sử backtracking thực hiện một số hành động tìm kiếm theo chiều sâu
    if state == goal_state:
        return [state]
    if depth_limit == 0:
        return None
    for neighbor in get_neighbors(state):
        result = backtracking(neighbor, goal_state, depth_limit - 1)
        if result:
            return [state] + result
    return None

def get_neighbors(state):
    neighbors = []
    rows, cols = 3, 3
    # Tìm vị trí của ô trống (0)
    for r in range(rows):
        for c in range(cols):
            if state[r][c] == 0:
                zero_r, zero_c = r, c
    moves = [(-1,0),(1,0),(0,-1),(0,1)]
    # Thực hiện các phép di chuyển
    for dr, dc in moves:
        nr, nc = zero_r + dr, zero_c + dc
        if 0 <= nr < 3 and 0 <= nc < 3:
            new_state = [list(row) for row in state]
            new_state[zero_r][zero_c], new_state[nr][nc] = new_state[nr][nc], new_state[zero_r][zero_c]
            neighbors.append(tuple(tuple(row) for row in new_state))
    return neighbors

def is_solvable(state):
    flat = [item for row in state for item in row]
    inversions = 0
    for i in range(len(flat)):
        if flat[i] == 0:
            continue
        for j in range(i + 1, len(flat)):
            if flat[j] == 0:
                continue
            if flat[i] > flat[j]:
                inversions += 1
    return inversions % 2 == 0

def backtracking_forward_checking(state, goal_state, path=None, visited=None, depth_limit=30):
    if path is None:
        path = [state]
    if visited is None:
        visited = set()
    if state == goal_state:
        return path
    if len(path) > depth_limit:
        return None
    visited.add(state)
    for neighbor in get_neighbors(state):
        if neighbor in visited:
            continue
        # Forward checking: chỉ tiếp tục nếu trạng thái neighbor có thể giải được
        if not is_solvable(neighbor):
            continue
        result = backtracking_forward_checking(neighbor, goal_state, path + [neighbor], visited, depth_limit)
        if result:
            return result
    visited.remove(state)
    return None
import copy

def forward_checking_search(goal_state, is_solvable_func, depth_limit=9):
    """
    Forward Checking Search cho CSP: Gán giá trị cho các ô từ ma trận rỗng với Forward Checking, MRV, và LCV.
    Trả về: path (danh sách trạng thái từ rỗng đến goal) hoặc None.
    """
    visited = set()
    explored_states = []
    path = []

    def is_valid_assignment(state, pos, value):
        # Không cho phép trùng giá trị
        for r in range(3):
            for c in range(3):
                if (r, c) != pos and state[r][c] == value:
                    return False
        return True

    def get_domain(state, pos, assigned):
        domain = []
        for value in range(9):
            if value not in assigned and is_valid_assignment(state, pos, value):
                domain.append(value)
        return domain

    def forward_check(state, pos, value, domains, assigned):
        i, j = pos
        new_domains = {k: v[:] for k, v in domains.items()}
        used_values = set(state[r][c] for r in range(3) for c in range(3) if state[r][c] is not None)
        related_positions = []
        if j > 0: related_positions.append((i, j - 1))
        if j < 2: related_positions.append((i, j + 1))
        if i > 0: related_positions.append((i - 1, j))
        if i < 2: related_positions.append((i + 1, j))
        for other_pos in related_positions:
            if other_pos not in assigned:
                r, c = other_pos
                new_domain = [val for val in new_domains[other_pos] if val not in used_values]
                new_domains[other_pos] = new_domain
                if not new_domain:
                    return False, domains
        return True, new_domains

    def select_mrv_variable(positions, domains, state):
        min_domain_size = float('inf')
        selected_pos = None
        for pos in positions:
            domain_size = len(domains[pos])
            if domain_size < min_domain_size:
                min_domain_size = domain_size
                selected_pos = pos
        return selected_pos

    def select_lcv_value(pos, domain, state, domains, assigned):
        value_scores = []
        for value in domain:
            temp_state = [row[:] for row in state]
            temp_state[pos[0]][pos[1]] = value
            _, new_domains = forward_check(temp_state, pos, value, domains, assigned)
            eliminated = sum(len(domains[p]) - len(new_domains[p]) for p in new_domains if p != pos)
            value_scores.append((eliminated, value))
        value_scores.sort()
        return [value for _, value in value_scores]

    def backtrack_with_fc(state, assigned, positions, domains):
        if len(assigned) == 9:
            state_tuple = tuple(tuple(row) for row in state)
            if state_tuple == goal_state and is_solvable_func(state):
                path.append(state_tuple)
                return path
            return None

        pos = select_mrv_variable(positions, domains, state)
        if pos is None:
            return None

        domain = get_domain(state, pos, set(assigned.values()))
        sorted_values = select_lcv_value(pos, domain, state, domains, assigned)
        state_tuple = tuple(tuple(row if row is not None else -1 for row in state_row) for state_row in state)
        if state_tuple in visited:
            return None
        visited.add(state_tuple)
        explored_states.append(state_tuple)

        for value in sorted_values:
            new_state = [row[:] for row in state]
            new_state[pos[0]][pos[1]] = value
            new_assigned = assigned.copy()
            new_assigned[pos] = value
            new_positions = [p for p in positions if p != pos]
            path.append(tuple(tuple(row if row is not None else -1 for row in new_state_row) for new_state_row in new_state))
            success, new_domains = forward_check(new_state, pos, value, domains, new_assigned)
            if success:
                result = backtrack_with_fc(new_state, new_assigned, new_positions, new_domains)
                if result is not None:
                    return result
            path.pop()
        return None

    empty_state = [[None for _ in range(3)] for _ in range(3)]
    positions = [(i, j) for i in range(3) for j in range(3)]
    domains = {(i, j): list(range(9)) for i in range(3) for j in range(3)}
    assigned = {}
    result = backtrack_with_fc(empty_state, assigned, positions, domains)
    return result, explored_states