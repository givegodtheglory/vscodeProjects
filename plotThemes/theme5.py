import matplotlib.pyplot as plt
import numpy as np
from cycler import cycler  # Import cycler explicitly to avoid errors

# --- 1. Global Color Definitions (Accessible everywhere) ---
vault_bg = '#202b38'      # Slate Navy
vault_gold = '#ffcc00'    # Vault-Tec Gold
text_white = '#ffffff'    # Pure White
grid_blue = '#3a4a5e'     # Structure Blue
alert_red = '#ff6666'     # Alert Red
data_blue = '#4db8ff'     # Data Blue

def apply_vault_overseer_theme():
    """Applies the theme using the global colors defined above."""
    plt.rcParams.update({
        # Backgrounds
        'figure.facecolor': vault_bg,
        'axes.facecolor': vault_bg,
        'savefig.facecolor': vault_bg,
        
        # Typography
        'font.family': 'monospace',
        'font.weight': 'normal',
        'font.size': 12,
        'text.color': text_white,
        'axes.labelcolor': text_white,
        'axes.titlecolor': text_white,
        'xtick.color': text_white,
        'ytick.color': text_white,
        
        # Grid
        'axes.grid': True,
        'grid.color': grid_blue,
        'grid.linestyle': '-',
        'grid.linewidth': 1.0,
        'grid.alpha': 0.5,
        
        # Borders
        'axes.edgecolor': text_white,
        'axes.linewidth': 1.5,
        'axes.spines.top': False,
        'axes.spines.right': False,
        
        # Line Colors
        'lines.linewidth': 2.5,
        'axes.prop_cycle': cycler(color=[vault_gold, data_blue, alert_red])
    })

# --- 2. Apply Theme ---
apply_vault_overseer_theme()

# --- 3. Generate Data ---
t = np.linspace(0, 1, 500)
# Binary Data: 0 1 0 1
data_signal = np.concatenate([np.zeros(125), np.ones(125), np.zeros(125), np.ones(125)])
# Carrier frequencies
f1, f2 = 10, 30 
carrier = np.sin(2 * np.pi * (f1 * (1-data_signal) + f2 * data_signal) * t)

# --- 4. Plotting ---
fig, ax = plt.subplots(figsize=(10, 6))

# Plot Analog Signal
ax.plot(t, carrier, label='TX_OUTPUT_SIGNAL')

# Plot Digital Steps
ax.step(t, data_signal * 1.5 - 2.5, where='post', color=data_blue, linewidth=2, label='BINARY_DATA')

# Styling
ax.set_title(">> VAULT-TEC COMMS: FSK MODULATION <<", fontweight='bold', pad=15)
ax.set_xlabel("TIME (SECONDS)")
ax.set_ylabel("AMPLITUDE (V)")

# Annotations (Now 'text_white' works because it is global)
ax.text(0.12, 0.8, "BIT: 0\n(10 Hz)", transform=ax.transAxes, color=text_white, ha='center')
ax.text(0.37, 0.8, "BIT: 1\n(30 Hz)", transform=ax.transAxes, color=text_white, ha='center')

# Legend
ax.legend(frameon=True, facecolor=vault_bg, edgecolor=text_white, loc='lower right')

# Axis adjustments
ax.set_ylim(-3, 2)
ax.set_yticks([-2.5, -1, 0, 1])
ax.set_yticklabels(['LOGIC', '-1V', '0V', '+1V'])

plt.tight_layout()
plt.show()