import numpy as np
import plotly.graph_objects as go

import plotly.io as pio
pio.renderers.default = "browser"

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

def animate_function_with_trace(func, trace, best_point, bounds=(-1, 1), grid_points=50):
    lower, upper = bounds
    x = np.linspace(lower, upper, grid_points)
    y = np.linspace(lower, upper, grid_points)
    X, Y = np.meshgrid(x, y)
    Z = np.array([[func([X[i,j], Y[i,j]]) for j in range(grid_points)] for i in range(grid_points)])
    
    # Create initial figure with surface and empty trace
    surface = go.Surface(x=X, y=Y, z=Z, colorscale='Viridis', opacity=0.8, name='Function')
    
    trace_points = go.Scatter3d(
        x=[],
        y=[],
        z=[],
        mode='lines+markers',
        marker=dict(size=5, color='red'),
        line=dict(color='red', width=3),
        name='Trace'
    )
    
    best = go.Scatter3d(
        x=[best_point[0]],
        y=[best_point[1]],
        z=[best_point[2]],
        mode='markers',
        marker=dict(size=10, color='blue', symbol='diamond'),
        name='Best point'
    )
    
    fig = go.Figure(data=[surface, trace_points, best])
    
    # Create animation frames
    frames = []
    for i in range(1, len(trace) + 1):
        frame = go.Frame(
            data=[
                surface,
                go.Scatter3d(
                    x=[p[0] for p in trace[:i]],
                    y=[p[1] for p in trace[:i]],
                    z=[p[2] for p in trace[:i]],
                    mode='lines+markers',
                    marker=dict(size=5, color='red'),
                    line=dict(color='red', width=3),
                    name='Trace'
                ),
                best
            ],
            name=str(i)
        )
        frames.append(frame)
    
    fig.frames = frames
    
    fig.update_layout(
        title_text=f"Optimization Progress",
        scene=dict(
            xaxis_title='X',
            yaxis_title='Y',
            zaxis_title='Z',
            camera=dict(
                eye=dict(x=1.5, y=1.5, z=1.3)
            )
        ),
        updatemenus=[{
            'type': 'buttons',
            'showactive': False,
            'buttons': [
                {
                    'label': '▶ Play',
                    'method': 'animate',
                    'args': [None, {
                        'frame': {'duration': 100, 'redraw': True},
                        'fromcurrent': True,
                        'mode': 'immediate',
                        'transition': {'duration': 0}
                    }]
                },
                {
                    'label': '⏸ Pause',
                    'method': 'animate',
                    'args': [[None], {
                        'frame': {'duration': 0, 'redraw': False},
                        'mode': 'immediate',
                        'transition': {'duration': 0}
                    }]
                },
                {
                    'label': '⏮ Reset',
                    'method': 'animate',
                    'args': [[frames[0].name], {
                        'frame': {'duration': 0, 'redraw': True},
                        'mode': 'immediate',
                        'transition': {'duration': 0}
                    }]
                }
            ],
            'x': 0.1,
            'y': 1.0,
            'xanchor': 'left',
            'yanchor': 'top'
        }],
        sliders=[{
            'active': 0,
            'steps': [
                {
                    'args': [[f.name], {
                        'frame': {'duration': 0, 'redraw': True},
                        'mode': 'immediate',
                        'transition': {'duration': 0}
                    }],
                    'label': str(i),
                    'method': 'animate'
                }
                for i, f in enumerate(frames)
            ],
            'x': 0.1,
            'len': 0.85,
            'xanchor': 'left',
            'y': 0,
            'yanchor': 'top',
            'pad': {'b': 10, 't': 50},
            'currentvalue': {
                'visible': True,
                'prefix': 'Step: ',
                'xanchor': 'right',
                'font': {'size': 16}
            },
            'transition': {'duration': 50}
        }]
    )
    
    fig.show()

def animate_tsp_best_route(cities, best_route):
    cities = np.array(cities)
    
    # Calculate total distance
    total_distance = 0
    for i in range(len(best_route)):
        city1 = cities[best_route[i]]
        city2 = cities[best_route[(i + 1) % len(best_route)]]
        total_distance += np.linalg.norm(city2 - city1)
    
    # Create base figure with all cities
    city_points = go.Scatter(
        x=cities[:, 0],
        y=cities[:, 1],
        mode='markers+text',
        marker=dict(size=12, color='blue', symbol='circle', line=dict(width=2, color='white')),
        text=[str(i) for i in range(len(cities))],
        textposition='top center',
        textfont=dict(size=10, color='black'),
        name='Cities'
    )
    
    # Initial empty route
    route_line = go.Scatter(
        x=[],
        y=[],
        mode='lines+markers',
        line=dict(color='red', width=3),
        marker=dict(size=8, color='red'),
        name='Route'
    )
    
    fig = go.Figure(data=[city_points, route_line])
    
    # Create animation frames - build route step by step
    frames = []
    
    # Frame 0: No route
    frames.append(go.Frame(
        data=[city_points, route_line],
        name='0'
    ))
    
    # Frames 1 to n: Add one edge at a time
    for step in range(1, len(best_route) + 1):
        # Get cities up to current step
        route_segment = best_route[:step]
        x = [cities[i, 0] for i in route_segment]
        y = [cities[i, 1] for i in route_segment]
        
        # If we've completed the tour, close the loop
        if step == len(best_route):
            x.append(cities[best_route[0], 0])
            y.append(cities[best_route[0], 1])
        
        frame = go.Frame(
            data=[
                city_points,
                go.Scatter(
                    x=x,
                    y=y,
                    mode='lines+markers',
                    line=dict(color='red', width=3),
                    marker=dict(size=8, color='red'),
                    name='Route'
                )
            ],
            name=str(step)
        )
        frames.append(frame)
    
    fig.frames = frames
    
    # Layout with animation controls
    fig.update_layout(
        title=f"Best TSP Route (Distance: {total_distance:.2f})",
        xaxis=dict(
            title="X", 
            range=[cities[:, 0].min() - 1, cities[:, 0].max() + 1],
            constrain='domain'
        ),
        yaxis=dict(
            title="Y", 
            range=[cities[:, 1].min() - 1, cities[:, 1].max() + 1],
            scaleanchor='x',
            scaleratio=1
        ),
        width=800,
        height=700,
        showlegend=True,
        margin=dict(t=100, b=150),
        updatemenus=[{
            'type': 'buttons',
            'showactive': False,
            'buttons': [
                {
                    'label': '▶ Play',
                    'method': 'animate',
                    'args': [None, {
                        'frame': {'duration': 500, 'redraw': True},
                        'fromcurrent': True,
                        'mode': 'immediate',
                        'transition': {'duration': 300}
                    }]
                },
                {
                    'label': '⏸ Pause',
                    'method': 'animate',
                    'args': [[None], {
                        'frame': {'duration': 0, 'redraw': False},
                        'mode': 'immediate',
                        'transition': {'duration': 0}
                    }]
                },
                {
                    'label': '⏮ Reset',
                    'method': 'animate',
                    'args': [[frames[0].name], {
                        'frame': {'duration': 0, 'redraw': True},
                        'mode': 'immediate',
                        'transition': {'duration': 0}
                    }]
                }
            ],
            'x': 0.1,
            'y': -0.25,
            'xanchor': 'left',
            'yanchor': 'top'
        }],
        sliders=[{
            'active': 0,
            'steps': [
                {
                    'args': [[f.name], {
                        'frame': {'duration': 0, 'redraw': True},
                        'mode': 'immediate',
                        'transition': {'duration': 0}
                    }],
                    'label': f'Step {i}' if i > 0 else 'Start',
                    'method': 'animate'
                }
                for i, f in enumerate(frames)
            ],
            'x': 0.1,
            'len': 0.85,
            'xanchor': 'left',
            'y': 0,
            'yanchor': 'top',
            'pad': {'b': 10, 't': 50},
            'currentvalue': {
                'visible': True,
                'prefix': 'Building Route: ',
                'xanchor': 'right',
                'font': {'size': 14}
            },
            'transition': {'duration': 300}
        }]
    )
    
    fig.show()