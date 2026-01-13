import numpy as np
import matplotlib.pyplot as plt
from matplotlib import cycler

# --- 1. THEME DEFINITION (Fat Man) ---
AMMO_CRATE_GREEN = '#2e3b2b'
STENCIL_YELLOW = '#f0c808'
CHALK_WHITE = '#e0e0e0'
DANGER_RED = '#ff3333'
ENGRAVED_BLACK = '#1a2118'

def apply_fatman_theme():
    """Activates the M-42 Fat Man visual specification."""
    plt.rcParams.update({
        'figure.facecolor': AMMO_CRATE_GREEN,
        'axes.facecolor': AMMO_CRATE_GREEN,
        'savefig.facecolor': AMMO_CRATE_GREEN,
        'font.family': 'monospace',
        'font.weight': 'bold',
        'font.size': 10,
        'text.color': STENCIL_YELLOW,
        'axes.labelcolor': STENCIL_YELLOW,
        'axes.titlecolor': STENCIL_YELLOW,
        'xtick.color': STENCIL_YELLOW,
        'ytick.color': STENCIL_YELLOW,
        'axes.grid': True,
        'grid.color': ENGRAVED_BLACK,
        'grid.linestyle': '-',
        'grid.linewidth': 1.5,
        'grid.alpha': 0.6,
        'axes.edgecolor': STENCIL_YELLOW,
        'axes.linewidth': 2.5,
        'axes.spines.top': True,
        'axes.spines.right': True,
        'lines.linewidth': 3.0,
        # Default cycle if no specific color is provided
        'axes.prop_cycle': cycler(color=[CHALK_WHITE, DANGER_RED, STENCIL_YELLOW])
    })

# --- 2. THE ORGANIZER ---
def auto_organize(xs, ys, layout, 
                  titles=None,         # Subplot Titles (Top of graph)
                  xtitles=None,        # X-Axis Labels
                  ytitles=None,        # Y-Axis Labels
                  legend_labels=None,  # Trace Names in Legend
                  colors=None,         # Specific colors per trace
                  linestyles=None,     # Line styles (e.g., '--', ':', '-')
                  **kwargs):           # Global fallbacks
    """
    Organizes data lists into the plot structure.
    All list arguments must match the order of the data in xs/ys.
    """
    structure = []
    idx = 0
    
    for count in layout:
        fig_list = []
        for _ in range(count):
            if idx < len(xs):
                d = {'x': xs[idx], 'y': ys[idx]}
                
                # --- Map Lists to Individual Plots ---
                if titles and idx < len(titles): d['title'] = titles[idx]
                if xtitles and idx < len(xtitles): d['xlabel'] = xtitles[idx]
                if ytitles and idx < len(ytitles): d['ylabel'] = ytitles[idx]
                if legend_labels and idx < len(legend_labels): d['legend_label'] = legend_labels[idx]
                if colors and idx < len(colors): d['color'] = colors[idx]
                if linestyles and idx < len(linestyles): d['linestyle'] = linestyles[idx]
                
                # Apply global defaults for anything missing
                for k, v in kwargs.items():
                    if k not in d: d[k] = v
                        
                fig_list.append(d)
                idx += 1
        structure.append(fig_list)
    return structure

# --- 3. THE PLOTTER ---
def plot_flex(figures_data, base_figsize=(10, 5), show=True):
    """
    Renders the figures. 
    Returns a list of tuples: [(Figure, [Axes]), ...]
    """
    apply_fatman_theme()
    created_figs = []
    
    for subplots_list in figures_data:
        n = len(subplots_list)
        # Create figure with dynamic height based on N subplots
        fig, axes = plt.subplots(n, 1, figsize=(base_figsize[0], base_figsize[1] * n))
        
        # Ensure axes is always a list
        if n == 1: axes = [axes]
        
        for ax, data in zip(axes, subplots_list):
            # --- PLOT THE DATA ---
            ax.plot(data['x'], data['y'], 
                    label=data.get('legend_label'),
                    color=data.get('color'),          # Uses specific color if provided
                    linestyle=data.get('linestyle', '-') # Uses specific style if provided
            )
            
            # --- APPLY LABELS (Uppercased) ---
            if data.get('title'): ax.set_title(f">> {data['title'].upper()} <<", fontweight='bold' ,pad=20)
            if data.get('xlabel'): ax.set_xlabel(data['xlabel'].upper(), fontweight='bold', fontsize=12)
            if data.get('ylabel'): ax.set_ylabel(data['ylabel'].upper(), fontweight='bold', fontsize=12)

            # --- LEGEND ---
            if data.get('legend_label'):
                leg = ax.legend(frameon=True, loc='center right')
                frame = leg.get_frame()
                frame.set_facecolor(ENGRAVED_BLACK)
                frame.set_edgecolor(STENCIL_YELLOW)

            # --- BRANDING ---
            ax.text(0.84, 0.1, "FATMAN INDUSTRIES", transform=ax.transAxes, 
                    fontsize=9, color=AMMO_CRATE_GREEN, fontweight='bold',
                    verticalalignment='top',
                    bbox=dict(facecolor=STENCIL_YELLOW, edgecolor=STENCIL_YELLOW, boxstyle='square,pad=0.2'))

        fig.tight_layout()
        created_figs.append((fig, axes))

    if show:
        plt.show()
    return created_figs

# 1. Activate Theme


# 2. Generate Dummy Data
t = np.linspace(0, 10, 100)
data_x = [t, t, t]
data_y = [np.sin(t), np.cos(t), t**2 * 0.1]

# 3. Define Attributes Lists (Order matches data_x/data_y)
my_titles   = ["Primary Oscillator", "Harmonic Distortion", "Thermal Runaway"]
my_legends  = ["OSC_ALPHA", "OSC_BETA", "TEMP_CRITICAL"]
my_xtitles  = ["Time (ms)", "Time (ms)", "Time (s)"]
my_ytitles  = ["Voltage (V)", "Voltage (V)", "Temp (C)"]
my_colors   = [CHALK_WHITE, STENCIL_YELLOW, DANGER_RED]
my_styles   = ['-', '--', ':']  # <--- Styles: Solid, Dashed, Dotted

# 4. Organize
figures = auto_organize(
    data_x, 
    data_y, 
    layout=[2, 1],             # Window 1 has 2 plots, Window 2 has 1 plot
    titles=my_titles,
    xtitles=my_xtitles,
    ytitles=my_ytitles,
    legend_labels=my_legends,
    colors=my_colors,
    linestyles=my_styles       # <--- Passing the styles list
)

# 5. Plot
plot_flex(figures)