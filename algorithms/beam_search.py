from utils import get_neighbors, heuristic

def beam_search(initial_state, goal_state, beam_width=2):
    # Tập các trạng thái đã thăm để tránh lặp lại
    visited = set()
    queue = [(heuristic(initial_state, goal_state), [initial_state])]  # Khởi tạo queue với trạng thái ban đầu

    while queue:
        # Lọc queue để chỉ giữ lại beam_width phần tử với heuristic tốt nhất
        queue = sorted(queue, key=lambda x: x[0])[:beam_width]
        next_level = []  # Dùng để lưu các trạng thái kế tiếp

        for _, path in queue:
            current = path[-1]  # Lấy trạng thái cuối cùng trong path

            # Kiểm tra nếu đã đạt đến trạng thái mục tiêu
            if current == goal_state:
                return path

            # Tránh lặp lại các trạng thái đã thăm
            if current in visited:
                continue
            visited.add(current)

            # Duyệt qua các trạng thái con (neighbors) của trạng thái hiện tại
            for neighbor in get_neighbors(current):
                if neighbor not in visited:
                    h = heuristic(neighbor, goal_state)  # Tính heuristic cho neighbor
                    next_level.append((h, path + [neighbor]))  # Thêm neighbor vào next_level

        # Cập nhật lại queue cho vòng lặp tiếp theo
        queue = next_level

    return None  # Nếu không tìm thấy đường đi tới mục tiêu
