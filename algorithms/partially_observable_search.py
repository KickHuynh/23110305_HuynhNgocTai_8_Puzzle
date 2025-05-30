from utils import get_neighbors, manhattan_heuristic
import heapq
from collections import deque
import random

def is_goal_belief(belief_states, goal_state):
    """Check if any state in the belief set matches the goal state"""
    return any(state == goal_state for state in belief_states)

def is_valid_state(state):
    return isinstance(state, (list, tuple)) and len(state) == 3 and all(isinstance(row, (list, tuple)) and len(row) == 3 for row in state)

def get_observable_states(state):
    # Kiểm tra kiểu dữ liệu và cấu trúc của state
    if not is_valid_state(state):
        print('LỖI: state không hợp lệ:', state, 'type:', type(state))
        return None
    for i in range(3):
        for j in range(3):
            if state[i][j] == 0:
                return (i, j)
    return None

def extract_state_from_belief(belief):
    # Nếu belief là tuple/list các state, lấy state đầu tiên hợp lệ
    if isinstance(belief, (list, tuple)):
        for state in belief:
            if is_valid_state(state):
                return state
    # Nếu belief bản thân là state 3x3
    if is_valid_state(belief):
        return belief
    return None

def partially_observable_search(initial_belief_states, goal_state):
    # Nếu đầu vào là 1 state 3x3, chuyển thành list chứa 1 state
    if isinstance(initial_belief_states, tuple) and len(initial_belief_states) == 3 and all(isinstance(row, tuple) and len(row) == 3 for row in initial_belief_states):
        initial_belief_states = [initial_belief_states]
    if not initial_belief_states:
        return []
    puzzle = Puzzle(initial_belief_states[0])
    visited = set()
    queue = deque([(puzzle, [puzzle])])
    while queue:
        current, path = queue.popleft()
        if current.state == goal_state:
            return [p.state for p in path]
        state_key = str(current.state)
        if state_key in visited:
            continue
        visited.add(state_key)
        possible_states = get_possible_states(current)
        for state in possible_states:
            new_puzzle = Puzzle(state)
            x0, y0 = new_puzzle.find_zero()
            for dx, dy in [(-1,0),(1,0),(0,-1),(0,1)]:
                nx, ny = x0+dx, y0+dy
                if 0<=nx<3 and 0<=ny<3:
                    next_puzzle = new_puzzle.copy()
                    if next_puzzle.move(nx, ny):
                        if str(next_puzzle.state) not in visited:
                            queue.append((next_puzzle, path + [next_puzzle]))
    return []

GOAL_STATE = ((1,2,3),(4,5,6),(7,8,0))

class Puzzle:
    def __init__(self, state):
        self.state = tuple(tuple(row) for row in state)
    def find_zero(self):
        for y in range(3):
            for x in range(3):
                if self.state[y][x] == 0:
                    return x, y
        return None
    def copy(self):
        return Puzzle([list(row) for row in self.state])
    def move(self, nx, ny):
        x0, y0 = self.find_zero()
        if 0 <= nx < 3 and 0 <= ny < 3:
            state_list = [list(row) for row in self.state]
            state_list[y0][x0], state_list[ny][nx] = state_list[ny][nx], state_list[y0][x0]
            self.state = tuple(tuple(row) for row in state_list)
            return True
        return False

def get_possible_states(puzzle):
    possible_states = []
    current_state = [list(row) for row in puzzle.state]
    for _ in range(3):
        new_state = [row[:] for row in current_state]
        non_zero_positions = [(x, y) for y in range(3) for x in range(3) if new_state[y][x] != 0]
        if len(non_zero_positions) >= 2:
            pos1, pos2 = random.sample(non_zero_positions, 2)
            new_state[pos1[1]][pos1[0]], new_state[pos2[1]][pos2[0]] = new_state[pos2[1]][pos2[0]], new_state[pos1[1]][pos1[0]]
            possible_states.append([row[:] for row in new_state])
    return possible_states