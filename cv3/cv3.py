import numpy as np
import random

def create_distance_matrix(cities):
    n = len(cities)
    matrix = np.zeros((n, n))

    for i in range(n):
        for j in range(n):
            if i != j:
                matrix[i][j] = np.linalg.norm(np.array(cities[i]) - np.array(cities[j]))
    return matrix

def create_route(city_count):
    route = list(range(city_count))
    random.shuffle(route)
    return route 

def select(cities):
    df = sum(i[1] for i in cities)
    probabilities = [i[1]/df for i in cities]
    chosen = np.random.choice(len(cities), len(cities), p=probabilities)
    return [cities[i][0] for i in chosen]

def rank_routes(population, matrix):
    results = {i: calculate_distance(route, matrix) for i, route in enumerate(population)}
    return sorted(results.items(), key=lambda x: x[1], reverse=True)

def ordered_crossover(parent1, parent2):
    start, end = sorted(random.sample(range(len(parent1)), 2))
    child = [None]*len(parent1)

    child[start:end] = parent1[start:end]

    p2_index = end
    for i in range(len(child)):
        if child[i] is None:
            while parent2[p2_index % len(parent2)] in child:
                p2_index += 1
            child[i] = parent2[p2_index % len(parent2)]
            p2_index += 1
    return child

def breed(mating_pool):
    children = []
    pool = random.sample(mating_pool, len(mating_pool))
    for i in range(len(mating_pool)):
        child = ordered_crossover(pool[i], pool[len(mating_pool)-i-1])
        children.append(child)
    return children

def mutate(individual, mutation_rate):
    for i in range(len(individual)):
        if random.random() < mutation_rate:
            swap_with = random.randint(0, len(individual)-1)
            individual[i], individual[swap_with] = individual[swap_with], individual[i]
    return individual

def mutate_population(population, mutation_rate):
    return [mutate(ind, mutation_rate) for ind in population]

def next_generation(current_gen, matrix, mutation_rate):
    ranked_routes = rank_routes(current_gen, matrix)
    selection_results = select(ranked_routes)
    mating_pool = [current_gen[i] for i in selection_results]
    children = breed(mating_pool)
    next_generation = mutate_population(children, mutation_rate)
    return next_generation


def calculate_distance(route, matrix):
    dist = sum(matrix[route[i], route[i+1]] for i in range(len(route)-1))
    dist += matrix[route[-1], route[0]] # návrat zpět
    return dist

def genetic_algorithm(cities, population_size, mutation_rate, generations):
    distances = create_distance_matrix(cities)
    population = [create_route(len(cities)) for _ in range(population_size)]

    for i in range(generations):
        population = next_generation(population, distances, mutation_rate)

    best_route_index = rank_routes(population, distances)[0][0]
    return population[best_route_index]