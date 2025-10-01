import numpy as np
import plotly.graph_objects as go

import plotly.io as pio
pio.renderers.default = "browser"

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