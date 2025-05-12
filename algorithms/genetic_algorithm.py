import random
from utils import get_neighbors

POPULATION_SIZE = 50
GENOME_LENGTH = 30
GENERATIONS = 500
MUTATION_RATE = 0.2
MAX_NO_IMPROVEMENT = 100

def flatten(state):
    return [num for row in state for num in row]

def hamming_distance(state, goal_state):
    flat_s = flatten(state)
    flat_g = flatten(goal_state)
    return sum(1 for a, b in zip(flat_s, flat_g) if a != b and a != 0)

def generate_candidate(initial_state, goal_state):
    path = [initial_state]
    current = initial_state
    visited = {current}
    for _ in range(GENOME_LENGTH):
        neighbors = [n for n in get_neighbors(current) if n not in visited]
        if not neighbors:
            break
        current = random.choice(neighbors)
        visited.add(current)
        path.append(current)
        if current == goal_state:
            break
    return path

def evaluate(candidate, goal_state):
    return -hamming_distance(candidate[-1], goal_state)

def crossover(p1, p2):
    min_len = min(len(p1), len(p2))
    split = random.randint(1, min_len - 1) if min_len > 1 else 1
    return p1[:split] + p2[split:]

def mutate(candidate):
    if len(candidate) < 2:
        return candidate
    idx = random.randint(1, len(candidate) - 1)
    base = candidate[idx - 1]
    visited = set(candidate[:idx])
    neighbors = [n for n in get_neighbors(base) if n not in visited]
    if not neighbors:
        return candidate
    new_state = random.choice(neighbors)
    return candidate[:idx] + [new_state]

def genetic_algorithm(initial_state, goal_state, population_size=POPULATION_SIZE, max_generations=GENERATIONS):
    population = [generate_candidate(initial_state, goal_state) for _ in range(population_size)]
    explored_states = []
    best_fitness = float('-inf')
    no_improvement_count = 0

    for generation in range(max_generations):
        population.sort(key=lambda c: evaluate(c, goal_state), reverse=True)
        explored_states.extend([c[-1] for c in population[:5]])
        best_candidate = population[0]
        current_fitness = evaluate(best_candidate, goal_state)

        if best_candidate[-1] == goal_state:
            return best_candidate, explored_states

        if current_fitness > best_fitness:
            best_fitness = current_fitness
            no_improvement_count = 0
        else:
            no_improvement_count += 1

        if no_improvement_count >= MAX_NO_IMPROVEMENT:
            break

        new_population = population[:population_size // 2]
        while len(new_population) < population_size:
            parent1, parent2 = random.sample(new_population, 2)
            child = crossover(parent1, parent2)
            if random.random() < MUTATION_RATE:
                child = mutate(child)
            new_population.append(child)
        population = new_population

    return None, explored_states