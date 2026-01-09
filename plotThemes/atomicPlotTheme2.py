import matplotlib.pyplot as plt
import numpy as np

def apply_blueprint_theme():
    # --- Color Palette (Blueprint) ---
    blueprint_bg = '#243447'    # Deep, cool midnight blue
    drafting_white = '#e0e6ed'  # Soft off-white for main lines
    measure_yellow = '#f0c674'  # Pale yellow for secondary data
    grid_color = '#4a5b6c'      # Low-contrast grey-blue
    
    plt.rcParams.update({
        # Backgrounds
        'figure.facecolor': blueprint_bg,
        'axes.facecolor': blueprint_bg,
        'savefig.facecolor': blueprint_bg,
        
        # Typography
        'font.family': 'monospace',
        'text.color': drafting_white,
        'axes.labelcolor': drafting_white,
        'axes.titlecolor': drafting_white,
        'xtick.color': drafting_white,
        'ytick.color': drafting_white,
        
        # The Grid (Subtle and structural)
        'axes.grid': True,
        'axes.grid.which': 'both',
        'grid.color': grid_color,
        'grid.linestyle': '-',
        'grid.linewidth': 0.8,
        'grid.alpha': 0.3,      # Very faint transparency
        
        # Borders
        'axes.edgecolor': drafting_white,
        'axes.linewidth': 1.5,
        'axes.spines.top': False,    # Remove top border for cleaner look
        'axes.spines.right': False,  # Remove right border
        
        # Lines
        'lines.linewidth': 2.0,
        'axes.prop_cycle': plt.cycler(color=[drafting_white, measure_yellow])
    })

# --- Demo ---
apply_blueprint_theme()

# Data
x = np.linspace(0, 10, 100)
y1 = np.sin(x) * 10
y2 = np.cos(x) * 10

fig, ax = plt.subplots(figsize=(10, 6))

# Plot Lines
ax.plot(x, y1, label='PRIMARY_COOLING')

# --- "Graph Paper" Grid (Reduced Noise) ---
ax.minorticks_on()
# Minor grid is barely visible, just for texture
ax.grid(which='minor', linestyle=':', linewidth=0.5, color='#4a5b6c', alpha=0.2)
ax.grid(which='major', linestyle='-', linewidth=1.0, color='#4a5b6c', alpha=0.4)

# Titles
ax.set_title("SCHEMATIC: FLUID DYNAMICS", loc='left', fontsize=14, pad=15, weight='bold')
ax.set_xlabel("FLOW RATE (m/s)", fontsize=11)
ax.set_ylabel("PRESSURE (kPa)", fontsize=11)

# Simple Legend (No box, cleaner look)
ax.legend(frameon=False, loc='upper right')

plt.tight_layout()
plt.show()