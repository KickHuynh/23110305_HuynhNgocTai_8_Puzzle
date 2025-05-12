from algorithms import and_or_search # This imports the module

# Global Goal State for belief scenarios (can be imported by app.py)
GOAL_STATE = ((1, 2, 3),
              (4, 5, 6),
              (7, 8, 0))

def and_or_search_path(start, goal):
    """
    Wrapper for the And-Or search algorithm.
    'start' is the initial state for this specific search.
    'goal' is the target goal state.
    """
    # Ensure that and_or_search.and_or_search is the actual function call
    # The imported 'and_or_search' is the module.
    print(f"and_or_search_path called with start: {start}, goal: {goal}")
    try:
        # Assuming and_or_search.py contains a function also named and_or_search
        result = and_or_search.and_or_search(start, goal)
        print(f"and_or_search_path result: {result}")
        return result
    except Exception as e:
        print(f"Error in and_or_search.and_or_search: {e}")
        import traceback
        traceback.print_exc()
        return None # Return None or an empty list on error


def test_beliefs(belief_states, goal_state_param, algorithm_func):
    """
    Tests a given algorithm over a set of belief states.
    'belief_states': A list of initial states.
    'goal_state_param': The single goal state for all beliefs.
    'algorithm_func': The search function to use (e.g., and_or_search_path).
    Returns a list of paths (or empty lists if no solution found for a belief).
    """
    results = []
    print(f"test_beliefs: Running algorithm for {len(belief_states)} belief states towards {goal_state_param}")
    for i, belief in enumerate(belief_states):
        print(f"  Testing belief {i+1}: {belief}")
        # Each algorithm (like and_or_search_path) should handle its own goal state logic.
        # Here, we pass the common goal_state_param.
        path = algorithm_func(belief, goal_state_param)
        if isinstance(path, list) and path: # A valid path was found
            results.append(path)
            print(f"    Path found for belief {i+1}: {len(path)} steps")
        else: # No path found, or algorithm returned None/empty
            results.append([]) # Append an empty list as a placeholder
            print(f"    No path found for belief {i+1}")
    return results