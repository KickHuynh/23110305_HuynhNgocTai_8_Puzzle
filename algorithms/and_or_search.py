from utils import get_neighbors

class Problem:
    def __init__(self, initial, goal):
        self.initial = initial
        self.goal = goal

    def goal_test(self, state):
        return state == self.goal

    def actions(self, state):
        return get_neighbors(state)

    def result(self, state, action):
        return action  # action chính là trạng thái mới

def and_or_search(initial_state, goal_state):
    problem = Problem(initial_state, goal_state)
    memo = {}
    plan = or_search(problem.initial, problem, [], memo)
    return plan

def or_search(state, problem, path, memo):
    if problem.goal_test(state):
        return [state]
    if state in path:
        return None  # tránh lặp lại
    if state in memo:
        return memo[state]
    for action in problem.actions(state):
        result_state = problem.result(state, action)
        plan = and_search([result_state], problem, path + [state], memo)
        if plan:
            memo[state] = [state] + plan
            return memo[state]
    memo[state] = None
    return None

def and_search(states, problem, path, memo):
    plans = []
    for s in states:
        plan = or_search(s, problem, path, memo)
        if not plan:
            return None
        plans.extend(plan[1:] if plans else plan)  # tránh lặp lại trạng thái đầu
    return plans
