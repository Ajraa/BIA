import sys
import os

# Přidá parent directory (kde je base složka) do Python path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import numpy as np
import base.functions as functions
import base.visualization as visualization

def firefly_algorithm(func, n_fireflies=25, max_iter=100, 
                     alpha=0.5, beta_0=1.0):
    # Get problem dimensions
    dim = len(func.bounds)
    
    lower_bounds = (func.bounds[0], func.bounds[0])
    upper_bounds = (func.bounds[1], func.bounds[1])

    # Initialize firefly positions randomly
    fireflies = np.random.uniform(lower_bounds, upper_bounds, (n_fireflies, dim))
    
    # Calculate initial fitness (light intensity)
    fitness = np.array([func.do(f) for f in fireflies])
    
    # Track the best solution
    best_idx = np.argmin(fitness)
    best_position = fireflies[best_idx].copy()
    best_fitness = fitness[best_idx]
    trace = []
    trace.append([(fireflies[p][0], fireflies[p][1], fitness[p]) for p in range(n_fireflies)])

    # Main optimization loop
    for iteration in range(max_iter):
        # Update alpha (optional: decrease over time)
        alpha_t = alpha * (1 - iteration / max_iter)
        
        # For each firefly
        for i in range(n_fireflies):
            # Compare with all other fireflies
            for j in range(n_fireflies):
                # Move firefly i towards j if j is brighter (has lower fitness for minimization)
                if fitness[j] < fitness[i]:
                    # Calculate distance between fireflies i and j
                    r = np.linalg.norm(fireflies[i] - fireflies[j])
                    
                    # Calculate attractiveness using β = β₀/(1+r)
                    beta = beta_0 / (1 + r)
                    
                    # Generate random step
                    epsilon = np.random.uniform(-0.5, 0.5, dim)
                    
                    # Update firefly position
                    fireflies[i] = (fireflies[i] + 
                                   beta * (fireflies[j] - fireflies[i]) + 
                                   alpha_t * epsilon)
                    
                    # Ensure firefly stays within bounds
                    fireflies[i] = np.clip(fireflies[i], lower_bounds, upper_bounds)
                    
                    # Update fitness
                    fitness[i] = func.do(fireflies[i])
        
        # Update best solution
        current_best_idx = np.argmin(fitness)
        if fitness[current_best_idx] < best_fitness:
            best_fitness = fitness[current_best_idx]
            best_position = fireflies[current_best_idx].copy()
        
        trace.append([(fireflies[p][0], fireflies[p][1], fitness[p]) for p in range(n_fireflies)])

    return trace, (best_position, best_fitness)


# Example usage
if __name__ == "__main__":
    fc = functions.function_dict["Griewank"]
    trace, best_point = firefly_algorithm(
        func=fc,
        n_fireflies=30,
        max_iter=50,
        alpha=0.5,
        beta_0=1.0
    )
    visualization.animate_particle_swarm(func=fc, trace=trace, best_result=best_point, grid_points=100);
    
   