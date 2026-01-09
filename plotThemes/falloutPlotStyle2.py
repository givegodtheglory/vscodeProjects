import matplotlib.pyplot as plt
import numpy as np
from cycler import cycler

def apply_grid_heavy_fallout_theme():
    # --- Color Palette ---
    terminal_green = '#1aff1a' 
    background = '#000b00' # Deep dark green/black
    
    # Data colors (High contrast against the green grid)
    data_colors = [
        '#1aff1a',  # Phosphor Green
        '#ffb347',  # New Vegas Amber
        '#00ffff',  # Cyan/Blue
    ]
    
    plt.rcParams.update({
        # Backgrounds
        'figure.facecolor': background,
        'axes.facecolor': background,
        
        # Text
        'font.family': 'monospace',
        'text.color': terminal_green,
        'axes.labelcolor': terminal_green,
        'xtick.color': terminal_green,
        'ytick.color': terminal_green,
        'axes.titlecolor': terminal_green,

        # The Grid (Restored & Prominent)
        'axes.grid': True,
        'grid.color': terminal_green,
        'grid.linestyle': ':',   # Dotted lines avoid looking like data
        'grid.linewidth': 1.0,
        'grid.alpha': 0.6,       # High visibility
        
        # Borders
        'axes.edgecolor': terminal_green,
        'axes.linewidth': 2,
        
        # Data Lines
        'axes.prop_cycle': cycler(color=data_colors),
        'lines.linewidth': 3,
    })

# --- Apply & Plot ---
apply_grid_heavy_fallout_theme()

# Data
x = np.linspace(0, 10, 25)
y1 = np.sin(x) * 10
y2 = np.cos(x) * 8 + 2

fig, ax = plt.subplots(figsize=(10, 6))

# Plotting
ax.plot(x, y1, label='RADIATION', marker='s', markeredgecolor='black')
ax.plot(x, y2, label='WATER_LVL', marker='o', markeredgecolor='black')

# Titles and Labels
ax.set_title(">> SECTOR_7_ANALYSIS <<", fontweight='bold', pad=20)
ax.set_xlabel("[ DISTANCE_KM ]")
ax.set_ylabel("[ INTENSITY ]")

# Legend with solid background to hide grid lines behind text
legend = ax.legend(frameon=True, loc='upper right')
frame = legend.get_frame()
frame.set_facecolor('#000b00')
frame.set_edgecolor('#1aff1a')
frame.set_linewidth(1.5)

plt.show()