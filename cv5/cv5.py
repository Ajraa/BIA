import random
import math

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

    bounds = [func.bounds, func.bounds]

    for _ in range(num_particles):
        position = [random.uniform(bounds[i][0], bounds[i][1]) for i in range(dim)]
        velocity = [random.uniform(-abs(bounds[i][1] - bounds[i][0]), abs(bounds[i][1] - bounds[i][0])) * 0.1 for i in range(dim)]
        particles.append(position)
        velocities.append(velocity)
        personal_best_positions.append(position[:])
        personal_best_scores.append(func(position))
    
    global_best_position = personal_best_positions[personal_best_scores.index(min(personal_best_scores))]
    global_best_score = min(personal_best_scores)
    
    for _ in range(max_iter):
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

                particles[i][d] = max(bounds[d][0], min(bounds[d][1], particles[i][d]))

            score = func(particles[i])
            trace.append((particles[i][:], score))
            if score < personal_best_scores[i]:
                personal_best_scores[i] = score
                personal_best_positions[i] = particles[i][:]

                if score < global_best_score:
                    global_best_score = score
                    global_best_position = particles[i][:]

    return trace, (global_best_position, global_best_score)