import numpy as np

def blind_search(func, lower_bound, upper_bound, points, repeats):
    max_value = None
    max_x = None
    max_y = None
    trace = []

    for i in range(repeats):
        x = np.linspace(lower_bound, upper_bound, points)
        y = np.linspace(lower_bound, upper_bound, points)

        for j in range(points):
            z = func(x[j], y[j])
            if z > max_value:
                max_value = z
                max_x = x[j]
                max_y = y[j]
                trace.append((max_value, max_x, max_y))

    return trace