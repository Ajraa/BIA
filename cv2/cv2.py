# Simulované žíhání (Simulated Annealing)
# U minina se začínají na vyšších teplotách
# čím více drasticky chladíme, tím více můžeme zamezit hledání do šířky a skončit v lokálním minimu
import sys
import os

# Přidá parent directory (kde je base složka) do Python path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import plotly.graph_objects as go
import numpy as np
import math
import base.functions as functions
import base.visualization as visualization

def simulated_annealing(func, initial_temp, min_temp, lower_bound, upper_bound, alpha, radius):
    temp = initial_temp

    min_x = np.random.uniform(lower_bound, upper_bound)
    min_y = np.random.uniform(lower_bound, upper_bound)
    min_value = func([min_x, min_y])
    trace = [(min_x, min_y, min_value)]

    while temp > min_temp:
        lower_bound_x = max(lower_bound, min_x - radius)
        upper_bound_x = min(upper_bound, min_x + radius)
        lower_bound_y = max(lower_bound, min_y - radius)
        upper_bound_y = min(upper_bound, min_y + radius)
        

        x = np.random.uniform(lower_bound_x, upper_bound_x)
        y = np.random.uniform(lower_bound_y, upper_bound_y)
        z = func([x, y])


        if z < min_value:
            min_value = z
            min_x = x
            min_y = y
            trace.append((min_x, min_y, min_value))
        else:
            r = np.random.rand()
            if r < math.e**(-(func([x, y]) - min_value)/temp):
                min_value = z
                min_x = x
                min_y = y
                trace.append((min_x, min_y, min_value))

        temp = temp * alpha

    return trace, (min_x, min_y, min_value)

trace, best_point = simulated_annealing(
    func=functions.sphere,
    initial_temp=50,
    min_temp=1e-4,
    lower_bound=-5.12,
    upper_bound=5.12, 
    alpha=0.95,
    radius=0.5
)

visualization.animate_function_with_trace(func=functions.sphere, trace=trace, best_point=best_point, bounds=(-5.12, 5.12), grid_points=100);