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

def calculate_distance(route, matrix):
    dist = sum(matrix[route[i], route[i+1]] for i in range(len(route)-1))
    dist += matrix[route[-1], route[0]] # návrat zpět
    return dist

def genetic_algorithm(cities, populatoin_size, mutation_rate, generations):
    distances = create_distance_matrix(cities)
    population = [create_route(len(cities)) for _ in range(populatoin_size)]

    for i in range(generations):
        break