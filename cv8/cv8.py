import sys
import os

# Přidá parent directory (kde je base složka) do Python path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import numpy as np
import base.functions as functions
import base.visualization as visualization

def firefly_algorithm(func, dim=2, n_fireflies=25, max_iter=100, 
                     alpha=0.5, beta_0=1.0):
    # Use provided dimensionality (dim) and function bounds
    lb, ub = func.bounds
    lower_bounds = np.array([lb] * dim)
    upper_bounds = np.array([ub] * dim)

    fireflies = np.random.uniform(lower_bounds, upper_bounds, (n_fireflies, dim))
    
    fitness = np.array([func.do(f) for f in fireflies])
    
    best_idx = np.argmin(fitness)
    best_position = fireflies[best_idx].copy()
    best_fitness = fitness[best_idx]
    trace = []
    trace.append([(fireflies[p][0], fireflies[p][1] if dim>1 else fireflies[p][0], fitness[p]) for p in range(n_fireflies)])

    for iteration in range(max_iter):
        # náhodný element zmenšující se s časem
        alpha_t = alpha * (1 - iteration / max_iter)
        
        for i in range(n_fireflies):
            # porovnání všech světlušek
            for j in range(n_fireflies):
                # pohyb světlušky i směrem k j, pokud je j jasnější
                if fitness[j] < fitness[i]:
                    # Calculate distance between fireflies i and j
                    r = np.linalg.norm(fireflies[i] - fireflies[j])
                    
                    # atraktivita
                    beta = beta_0 / (1 + r)
                    
                    # směr kroku
                    epsilon = np.random.uniform(-0.5, 0.5, dim)
                    
                    fireflies[i] = (fireflies[i] + 
                                   beta * (fireflies[j] - fireflies[i]) + 
                                   alpha_t * epsilon)
                    fireflies[i] = np.clip(fireflies[i], lower_bounds, upper_bounds)
                    
                    fitness[i] = func.do(fireflies[i])
        
        current_best_idx = np.argmin(fitness)
        if fitness[current_best_idx] < best_fitness:
            best_fitness = fitness[current_best_idx]
            best_position = fireflies[current_best_idx].copy()
        
        trace.append([(fireflies[p][0], fireflies[p][1], fitness[p]) for p in range(n_fireflies)])

    return trace, (best_position, best_fitness)


if __name__ == "__main__":
    fc = functions.function_dict["Michalewicz"]
    trace, best_point = firefly_algorithm(
        func=fc,
        n_fireflies=50,
        max_iter=50,
        alpha=1.0,
        beta_0=1.0
    )
    visualization.animate_particle_swarm(func=fc, trace=trace, best_result=best_point, grid_points=100, title="Firefly Optimization");
    
   