import matplotlib.pyplot as plt
import numpy as np
from cycler import cycler

# --- 1. The Flexible Plotter ---
def plot_flex(figures_data, base_figsize=(10, 4), show=True):
    # --- Global Color Palette (Military Spec) ---
    ammo_crate_green = '#2e3b2b'  # Dark Olive Drab (Matte background)
    stencil_yellow = '#f0c808'    # Warning Label Yellow
    chalk_white = '#e0e0e0'       # Faded white (for main data)
    danger_red = '#ff3333'        # Critical Levels
    engraved_black = '#1a2118'    # Dark grid (looks like grooves in metal)

    plt.rcParams.update({
        # Backgrounds (Matte Metal)
        'figure.facecolor': ammo_crate_green,
        'axes.facecolor': ammo_crate_green,
        'savefig.facecolor': ammo_crate_green,
        
        # Typography (Stencil/Warning Style)
        'font.family': 'monospace',
        'font.weight': 'bold',        # Bold text mimics stencils
        'font.size': 11,
        'text.color': stencil_yellow,
        'axes.labelcolor': stencil_yellow,
        'axes.titlecolor': stencil_yellow,
        'xtick.color': stencil_yellow,
        'ytick.color': stencil_yellow,
        
        # The Grid (Engraved Look)
        # We make the grid DARKER than the background
        'axes.grid': True,
        'grid.color': engraved_black,
        'grid.linestyle': '-',
        'grid.linewidth': 1.5,
        'grid.alpha': 0.6,
        
        # Borders (Heavy Industrial)
        'axes.edgecolor': stencil_yellow,
        'axes.linewidth': 2.5,
        'axes.spines.top': True,     # Boxed in like a crate
        'axes.spines.right': True,
        
        # Data Lines (Chalk & Paint)
        'lines.linewidth': 3.0,
        'axes.prop_cycle': cycler(color=[chalk_white, danger_red, stencil_yellow])
    })  
    
    created_figs = []
    
    for subplots_list in figures_data:
        n = len(subplots_list)
        fig, axes = plt.subplots(n, 1, figsize=(base_figsize[0], base_figsize[1] * n))
        
        if n == 1: axes = [axes]
        
        for ax, data in zip(axes, subplots_list):
            # Plot the data
            ax.plot(data['x'], data['y'], 
                    color=data.get('color', 'blue'),
                    linestyle=data.get('linestyle', '-'),
                    label=data.get('legend_label')) # Optional legend
            
            # --- APPLY LABELS & TITLES ---
            ax.set_title(data.get('title', ''))
            ax.set_xlabel(data.get('xlabel', '')) 
            ax.set_ylabel(data.get('ylabel', ''))
            
            if data.get('legend_label'):
                ax.legend()
                
            ax.grid(True, alpha=0.3)
            
        fig.tight_layout()
        created_figs.append((fig, axes))

    if show:
        plt.show()
    return created_figs

# --- 2. The Organizer (Now accepts lists for labels) ---
def auto_organize(xs, ys, layout, titles=None, xlabels=None, ylabels=None, **kwargs):
    """
    xs, ys: Lists of data arrays.
    titles, xlabels, ylabels: Lists of strings (order must match data).
    kwargs: Applied to ALL plots (e.g., color='red').
    """
    structure = []
    idx = 0
    
    for count in layout:
        fig_list = []
        for _ in range(count):
            if idx < len(xs):
                d = {'x': xs[idx], 'y': ys[idx]}
                
                # Assign specific labels if the lists exist and have enough items
                if titles and idx < len(titles): 
                    d['title'] = titles[idx]
                if xlabels and idx < len(xlabels): 
                    d['xlabel'] = xlabels[idx]
                if ylabels and idx < len(ylabels): 
                    d['ylabel'] = ylabels[idx]
                
                # Apply global styles
                d.update(kwargs)
                fig_list.append(d)
                idx += 1
        structure.append(fig_list)
        
    return structure

# --- 3. Example Usage ---

# Data
t = np.linspace(0, 10, 100)
data_x = [t, t, t]
data_y = [np.sin(t), np.cos(t), t**2]

# Labels (Make lists that match the order of your data)
my_titles = ["Sine Wave", "Cosine Wave", "Parabola"]
my_x_labels = ["Time (s)", "Time (s)", "Distance (m)"]
my_y_labels = ["Voltage (V)", "Current (A)", "Height (m)"]

# We pass the lists of labels into the function
figures = auto_organize(
    data_x, 
    data_y, 
    layout=[2, 1], 
    titles=my_titles, 
    xlabels=my_x_labels, 
    ylabels=my_y_labels,
    color='purple' # Global style
)
plot_flex(figures)