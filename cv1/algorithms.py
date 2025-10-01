import numpy as np
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import base.functions as functions
import base.visualization as visualization

def blind_search(func, lower_bound, upper_bound, iterations):
    min_value = np.inf
    min_x = None
    min_y = None
    trace = []

    x = np.random.uniform(lower_bound, upper_bound, iterations)
    y = np.random.uniform(lower_bound, upper_bound, iterations)

    for i in range(iterations):
        z = func([x[i], y[i]])
        trace.append((x[i], y[i], z))

        if z < min_value:
            min_value = z
            min_x = x[i]
            min_y = y[i]

    return trace, (min_x, min_y, min_value)

def hillclimbing(func, lower_bound, upper_bound, iterations, radius, points_per_iteration = 20):
    min_x = np.random.uniform(lower_bound, upper_bound)
    min_y = np.random.uniform(lower_bound, upper_bound)
    min_value = func([min_x, min_y])
    trace = [(min_x, min_y, min_value)]

    lower_bound_x = lower_bound
    lower_bound_y = lower_bound
    upper_bound_x = upper_bound
    upper_bound_y = upper_bound

    for _ in range(iterations):
        lower_bound_x = max(lower_bound, min_x - radius)
        upper_bound_x = min(upper_bound, min_x + radius)
        lower_bound_y = max(lower_bound, min_y - radius)
        upper_bound_y = min(upper_bound, min_y + radius)
        
        xs = np.random.uniform(lower_bound_x, upper_bound_x, points_per_iteration)
        ys = np.random.uniform(lower_bound_y, upper_bound_y, points_per_iteration)
        zs = np.array([func([xs[i], ys[i]]) for i in range(points_per_iteration)])

        index = np.argmin(zs)
        if zs[index] < min_value:
            min_value = zs[index]
            min_x = xs[index]
            min_y = ys[index]
            trace.append((min_x, min_y, min_value))

    return trace, (min_x, min_y, min_value)

#trace, best_point = blind_search(functions.sphere, lower_bound=-5.12, upper_bound=5.12, iterations=50)
trace, best_point = hillclimbing(functions.sphere, lower_bound=-5.12, upper_bound=5.12, iterations=50, radius=0.2)
visualization.plot_function_with_trace(functions.sphere, trace, best_point, bounds=(-5.12, 5.12))
