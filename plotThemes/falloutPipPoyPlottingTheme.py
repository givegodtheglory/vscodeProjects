import matplotlib.pyplot as plt
import matplotlib.style as style
import numpy as np

def apply_fallout_theme():
    """Applies a Fallout Pip-Boy aesthetic to Matplotlib."""
    
    # Color Palette (Phosphor Green)
    phosphor_green = '#1aff1a'  # Bright neon green
    dark_green_bg = '#000b00'   # Very dark green/black
    grid_color = '#2a4d2a'      # Dimmer green for grids

    # Update rcParams
    fallout_params = {
        # Backgrounds
        'figure.facecolor': dark_green_bg,
        'axes.facecolor': dark_green_bg,
        'savefig.facecolor': dark_green_bg,
        
        # Text and Labels
        'text.color': phosphor_green,
        'axes.labelcolor': phosphor_green,
        'xtick.color': phosphor_green,
        'ytick.color': phosphor_green,
        'axes.titlecolor': phosphor_green,
        'font.family': 'monospace',  # Retro terminal look
        
        # Spines (Borders)
        'axes.edgecolor': phosphor_green,
        'axes.linewidth': 2,         # Thicker, bolder borders
        
        # Grid
        'axes.grid': True,
        'grid.color': grid_color,
        'grid.linestyle': '--',
        'grid.linewidth': 0.8,
        'grid.alpha': 0.8,
        
        # Lines and Markers
        'lines.linewidth': 2,
        'lines.color': phosphor_green,
        'lines.marker': 's',         # Square markers feel more 'digital'
        'patch.edgecolor': phosphor_green,
    }
    
    plt.rcParams.update(fallout_params)

# --- Demo the Theme ---

# 1. Apply the theme
apply_fallout_theme()

# 2. Generate Data
x = np.linspace(0, 10, 20)
y1 = np.sin(x)
y2 = np.cos(x)

# 3. Plot
fig, ax = plt.subplots(figsize=(10, 6))

# Plot lines with a slight "glow" effect (simulated by plotting twice)
# Thick transparent line underneath, thin bright line on top
ax.plot(x, y1, color='#1aff1a', linewidth=4, alpha=0.3) 
ax.plot(x, y1, label='RADIATION_LVL', color='#1aff1a', linewidth=2)

ax.plot(x, y2, color='#1aff1a', linewidth=4, alpha=0.3, linestyle=':')
ax.plot(x, y2, label='OXYGEN_SAT', color='#1aff1a', linewidth=2, linestyle=':')

# Styling
ax.set_title(">> PIP-BOY 3000 INTERFACE <<", fontsize=16, fontweight='bold', pad=20)
ax.set_xlabel("[ TIME_ELAPSED_SEC ]")
ax.set_ylabel("[ SIGNAL_STRENGTH ]")
ax.legend(frameon=True, facecolor='#000b00', edgecolor='#1aff1a')

# Add some "Scanline" text annotation
plt.text(0.02, 0.95, "SYS_STATUS: ONLINE", transform=ax.transAxes, fontsize=10)

plt.show()