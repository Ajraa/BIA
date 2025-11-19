import sys
import os

# Přidá parent directory (kde je base složka) do Python path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import base.functions as functions
import base.visualization as visualization
import random


def particle_swarm_optimization(
    func, 
    dim = 2, 
    num_particles=30, 
    max_iter=100, 
    inertia=0.7, 
    cognitive=1.5, 
    social=1.5
):  
    particles = []
    velocities = []
    personal_best_positions = []
    personal_best_scores = []
    trace = []
    # use function bounds for all dimensions
    lb, ub = func.bounds

    for _ in range(num_particles):
        position = [random.uniform(lb, ub) for _ in range(dim)]
        velocity = [random.uniform(-abs(ub - lb), abs(ub - lb)) * 0.1 for _ in range(dim)]
        particles.append(position)
        velocities.append(velocity)
        personal_best_positions.append(position[:])
        personal_best_scores.append(func.do(position))

    trace.append([(particles[i][0], particles[i][1], personal_best_scores[i]) for i in range(num_particles)])
 
    global_best_position = personal_best_positions[personal_best_scores.index(min(personal_best_scores))]
    global_best_score = min(personal_best_scores)
    
    for _ in range(max_iter):
        iter_trace = []
        for i in range(num_particles):
            for d in range(dim):
                r1 = random.random()
                r2 = random.random()
                velocities[i][d] = (
                    inertia * velocities[i][d]
                    + cognitive * r1 * (personal_best_positions[i][d] - particles[i][d])
                    + social * r2 * (global_best_position[d] - particles[i][d])
                )
                particles[i][d] += velocities[i][d]

                particles[i][d] = max(lb, ub, particles[i][d])

            score = func.do(particles[i])
            iter_trace.append((particles[i][0], particles[i][1], score))
            if score < personal_best_scores[i]:
                personal_best_scores[i] = score
                personal_best_positions[i] = particles[i][:]

                if score < global_best_score:
                    global_best_score = score
                    global_best_position = particles[i][:]
        trace.append(iter_trace)

    return trace, (global_best_position, global_best_score)

if __name__ == "__main__":
    fc = functions.function_dict["Michalewicz"]
    trace, best_point = particle_swarm_optimization(func=fc, dim=2, num_particles=30, max_iter=100)
    print(len(trace))
    #visualization.animate_particle_swarm(func=fc, trace=trace, best_result=best_point, grid_points=100);