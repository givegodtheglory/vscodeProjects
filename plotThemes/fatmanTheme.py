import matplotlib.pyplot as plt
import numpy as np
from cycler import cycler

# --- Global Color Palette (Military Spec) ---
ammo_crate_green = '#2e3b2b'  # Dark Olive Drab (Matte background)
stencil_yellow = '#f0c808'    # Warning Label Yellow
chalk_white = '#e0e0e0'       # Faded white (for main data)
danger_red = '#ff3333'        # Critical Levels
engraved_black = '#1a2118'    # Dark grid (looks like grooves in metal)

def apply_fatman_theme():
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

# --- Demo: Critical Mass Simulation ---
apply_fatman_theme()

# Generate Data
x = np.linspace(0, 10, 100)
neutron_flux = 2 * np.exp(0.3 * x)          # Exponential growth
control_rod = 50 * np.ones_like(x)          # Flat line
control_rod[50:] = 50 - 3 * (x[50:] - 5)**2 # Rods dropping

fig, ax = plt.subplots(figsize=(10, 6))

# Plot
ax.plot(x, neutron_flux, label='NEUTRON_FLUX')
ax.plot(x, control_rod, label='ROD_POSITION', linestyle='--')

# Styling
ax.set_title(">> M-42 FAT MAN: LAUNCH PARAMETERS <<", fontweight='bold', pad=20)
ax.set_xlabel("TIME, SECONDS", fontweight='bold', fontsize=12)
ax.set_ylabel("AMPLITUDE, dB", fontweight='bold', fontsize=12)

# "Stencil" Box Annotation
# This looks like a spray-painted warning on the side of the bomb
ax.text(0.7, 0.1, "FATMAN INDUSTRIES", 
        transform=ax.transAxes, 
        fontsize=12, color=ammo_crate_green, fontweight='bold',
        bbox=dict(facecolor=stencil_yellow, edgecolor=stencil_yellow, boxstyle='square,pad=0.4'))

# Legend (Dark background to pop against the olive)
legend = ax.legend(frameon=True, loc='center right')
frame = legend.get_frame()
frame.set_facecolor(engraved_black)
frame.set_edgecolor(stencil_yellow)

plt.tight_layout()
plt.show()