import numpy as np
import plotly.graph_objects as go

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import base.functions as functions

import plotly.io as pio
pio.renderers.default = "browser"

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

def plot_function_with_trace(func, trace, best_point, bounds=(-1, 1), grid_points=50):
    lower, upper = bounds
    x = np.linspace(lower, upper, grid_points)
    y = np.linspace(lower, upper, grid_points)
    X, Y = np.meshgrid(x, y)
    Z = np.array([[func([X[i,j], Y[i,j]]) for j in range(grid_points)] for i in range(grid_points)])
    
    surface = go.Surface(x=X, y=Y, z=Z, colorscale='Viridis', opacity=0.8)
    
    trace_points = go.Scatter3d(
        x=[p[0] for p in trace],
        y=[p[1] for p in trace],
        z=[p[2] for p in trace],
        mode='markers',
        marker=dict(size=5, color='red'),
        name='Trace'
    )
    
    best = go.Scatter3d(
        x=[best_point[0]],
        y=[best_point[1]],
        z=[best_point[2]],
        mode='markers',
        marker=dict(size=8, color='blue'),
        name='Best point'
    )
    
    fig = go.Figure(data=[surface, trace_points, best])
    fig.update_layout(scene=dict(
        xaxis_title='X',
        yaxis_title='Y',
        zaxis_title='Z'
    ))
    fig.show()

#trace, best_point = blind_search(functions.sphere, lower_bound=-5.12, upper_bound=5.12, iterations=50)
trace, best_point = hillclimbing(functions.sphere, lower_bound=-5.12, upper_bound=5.12, iterations=50, radius=0.2)
plot_function_with_trace(functions.sphere, trace, best_point, bounds=(-5.12, 5.12))
