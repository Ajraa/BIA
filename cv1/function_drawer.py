import sys
import os

# Přidá parent directory (kde je base složka) do Python path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import base.functions as functions
from base.function import Function
import math

import plotly.io as pio
pio.renderers.default = "browser"

def plot_different_ranges(functions):
    specs = [[{"type": "surface"}, {"type": "xy"}] for _ in functions]
    
    subplot_titles = []
    for func in functions:
        subplot_titles.extend([f"{func.name} ({func.bounds[0]} - {func.bounds[1]})", f"{func.name} - Contour"])
    
    fig = make_subplots(
        rows=len(functions), cols=2,
        specs=specs,
        subplot_titles=subplot_titles,
        vertical_spacing=0.03,
        horizontal_spacing=0.05,
        column_widths=[0.6, 0.4]
    )

    for i, func in enumerate(functions):
        x = np.linspace(func.bounds[0], func.bounds[1], func.points)
        y = np.linspace(func.bounds[0], func.bounds[1], func.points)
        X, Y = np.meshgrid(x, y)
        Z = np.array([[func.do(xi, yi) for xi in x] for yi in y])
        
        fig.add_trace(
            go.Surface(x=X, y=Y, z=Z, colorscale="Viridis", showscale=False), 
            row=i+1, col=1
        )
        
        fig.add_trace(
            go.Contour(x=x, y=y, z=Z, colorscale="Viridis", showscale=False), 
            row=i+1, col=2
        )

    fig.update_layout(
        height=500 * len(functions),
        width=1400,
        title_text="Optimalizační funkce - 3D Surface a Contour grafy",
        showlegend=False
    )
    
    fig.show()


plot_different_ranges(functions.fcs)