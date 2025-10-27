import sys
import os

# Přidá parent directory (kde je base složka) do Python path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import base.functions as functions
import base.visualization as visualization
import numpy as np


def soma(func, pop_size=30, dim=2, path_length=3.0, step=0.11, prt=0.1, migrations=100, min_div=1e-5):
    bounds = func.bounds
    pop = np.random.uniform(bounds[0], bounds[1], (pop_size, dim))
    fitness = np.apply_along_axis(func.do, 1, pop)
    best_idx = np.argmin(fitness)
    best = pop[best_idx].copy()
    best_fitness = fitness[best_idx]
    trace = []

    for _ in range(migrations):
        for i in range(pop_size):
            if i == best_idx:
                continue

            PRTVector = (np.random.rand(dim) < prt).astype(int)
            t = 0.0
            while t <= path_length:
                new_pos = pop[i] + (best - pop[i]) * PRTVector * t
                new_pos = np.clip(new_pos, bounds[0], bounds[1])
                new_fit = func.do(new_pos)
                if new_fit < fitness[i]:
                    pop[i] = new_pos
                    fitness[i] = new_fit
                t += step

        best_idx = np.argmin(fitness)
        if fitness[best_idx] < best_fitness:
            best_fitness = fitness[best_idx]
            best = pop[best_idx].copy()

        div = np.mean(np.std(pop, axis=0))
        if div < min_div:
            break
        trace.append([(pop[p][0], pop[p][1], fitness[p]) for p in range(pop_size)])


    return trace, (best, best_fitness)

fc = functions.function_dict["Griewank"]
trace, best_point = soma(
    func=fc,
    dim=2
)
print(len(trace))
visualization.animate_particle_swarm(func=fc, trace=trace, best_result=best_point, grid_points=100, title="SOMA Optimization");