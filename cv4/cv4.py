import sys
import os

# Přidá parent directory (kde je base složka) do Python path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import base.functions as functions
import numpy as np


def initialize_population(size, dim, lb, ub, func):
    pop = np.random.uniform(lb, ub, (size, dim))
    fitness = np.array([func(ind) for ind in pop]) # hodnota c9lové funkce pro každého jedince
    return pop, fitness

def generate_params(M_F, M_CR, H):
    r = np.random.randint(H)
    F = np.random.standard_cauchy() * 0.1 + M_F[r] # cauchy generuje více extrémních hodnot, to podpoří exploraci ale nechceme ji často, proto 0.1
    while F <= 0:
        F = np.random.standard_cauchy() * 0.1 + M_F[r]
    F = min(F, 1)

    CR = np.random.normal(M_CR[r], 0.1)
    CR = np.clip(CR, 0, 1)
    return F, CR

def mutate_and_crossover(pop, pop_size, fitness, F, CR, lb, ub, dim):
    new_pop = np.zeros_like(pop)

    for i in range(pop_size):
        p = max(2, int(0.2 * pop_size))
        p_best_idx = np.random.choice(np.argsort(fitness)[:p])
        r1, r2 = np.random.choice([x for x in range(pop_size) if x != i], 2, replace=False)

        x_i = pop[i]
        x_pbest = pop[p_best_idx]
        x_r1, x_r2 = pop[r1], pop[r2]

        v = x_i + F * (x_pbest - x_i) + F * (x_r1 - x_r2)
        v = np.clip(v, lb, ub)

        j_rand = np.random.randint(dim)
        u = np.array([v[j] if np.random.rand() < CR or j == j_rand else x_i[j] for j in range(dim)])
        new_pop[i] = u
    return new_pop

def shade(func, pop_size=20, dim=3, max_gen=1000, H=10, lb=-5, ub=5):
    pop, fitness = initialize_population(pop_size, dim, lb, ub, func)
    M_F = np.full(H, 0.5)
    M_CR = np.full(H, 0.5)
    k = 0

    for gen in range(max_gen):
        new_pop = np.zeros_like(pop)
        S_F, S_CR, delta_f = [], [], []

        for i in range(pop_size):
            F, CR = generate_params(M_F, M_CR, H)
            offspring = mutate_and_crossover(pop, pop_size, fitness, F, CR, lb, ub, dim)[i]
            print(offspring)
            offspring_fitness = func(offspring)

            if offspring_fitness < fitness[i]:
                new_pop[i] = offspring
                delta_f.append(fitness[i] - offspring_fitness)
                S_F.append(F)
                S_CR.append(CR)
        
        pop = new_pop
        fitness = np.array([func(ind) for ind in pop])

        if len(S_F) > 0:
            w = np.array(delta_f) / sum(delta_f)
            M_F[k] = np.sum(w * np.array(S_F)**2) / np.sum(w * np.array(S_F))
            M_CR[k] = np.sum(w * np.array(S_CR))
            k = (k + 1) % H
            
    best_idx = np.argmin(fitness)
    return pop[best_idx], fitness[best_idx]


shade(functions.sphere)