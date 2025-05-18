from utils import get_neighbors, heuristic

def beam_search(initial_state, goal_state, beam_width=2):
    visited = set()
    queue = [(heuristic(initial_state, goal_state), [initial_state])]  # Khởi tạo queue với trạng thái ban đầu

    while queue:
        queue = sorted(queue, key=lambda x: x[0])[:beam_width]
        next_level = []  # Dùng để lưu các trạng thái kế tiếp

        for _, path in queue:
            current = path[-1]  # Lấy trạng thái cuối cùng trong path

            if current == goal_state:
                return path

            if current in visited:
                continue
            visited.add(current)

            for neighbor in get_neighbors(current):
                if neighbor not in visited:
                    h = heuristic(neighbor, goal_state)  # Tính heuristic cho neighbor
                    next_level.append((h, path + [neighbor]))  # Thêm neighbor vào next_level

        queue = next_level

    return None  
