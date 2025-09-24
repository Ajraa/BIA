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
        subplot_titles.extend([f"{func.name} - 3D Surface", f"{func.name} - Contour"])
    
    fig = make_subplots(
        rows=len(functions), cols=2,
        specs=specs,
        subplot_titles=subplot_titles,
        vertical_spacing=0.03,
        horizontal_spacing=0.05,
        column_widths=[0.6, 0.4]
    )

    for i, func in enumerate(functions):
        x = np.linspace(func.lower_bound, func.upper_bound, func.points)
        y = np.linspace(func.lower_bound, func.upper_bound, func.points)
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
        height=500 * len(functions),  # Větší výška pro každou funkci
        width=1400,  # Větší celková šířka
        title_text="Optimalizační funkce - 3D Surface a Contour grafy",
        showlegend=False
    )
    
    fig.show()

fcs = [
    Function(functions.sphere, "Sphere", -5.12, 5.12, 100),
    Function(functions.ackley, "Ackley", -32.768, 32.768, 100),
    Function(functions.rastrigin, "Rastrigin", -5.12, 5.12, 100),
    Function(functions.rosenbrock, "Rosenbrock", -2.048, 2.048, 100),
    Function(functions.griewank, "Griewank", -600, 600, 100),
    Function(functions.schwefel, "Schwefel", -500, 500, 100),
    Function(functions.levy, "Levy", -10, 10, 100),
    Function(functions.michalewicz, "Michalewicz", 0, math.pi, 100),
    Function(functions.zakharov, "Zakharov", -5, 10, 100)
]

plot_different_ranges(fcs)