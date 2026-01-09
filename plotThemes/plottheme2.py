import matplotlib.pyplot as plt
import numpy as np

def apply_mojave_theme():
    # --- Color Palette (Amber Monochrome) ---
    crt_bg = '#140c00'        # Deep brownish-black (Warm dark)
    grid_color = '#4d3300'    # Dim amber grid
    text_color = '#ffcc99'    # Pale peach/amber for text (readable)
    
    # Data Colors
    primary_amber = '#ffb300' # Main signal
    secondary_amber = '#cc6600' # Reference/Background signal
    
    plt.rcParams.update({
        # Backgrounds
        'figure.facecolor': crt_bg,
        'axes.facecolor': crt_bg,
        'savefig.facecolor': crt_bg,
        
        # Typography
        'font.family': 'monospace', # Consolas or Courier ideally
        'font.size': 11,
        'text.color': text_color,
        'axes.labelcolor': text_color,
        'axes.titlecolor': text_color,
        'xtick.color': text_color,
        'ytick.color': text_color,
        
        # The Grid (Dashed for that "Old Western" tech feel)
        'axes.grid': True,
        'grid.color': grid_color,
        'grid.linestyle': '--',   
        'grid.linewidth': 0.8,
        'grid.alpha': 0.8,
        
        # Borders
        'axes.edgecolor': primary_amber,
        'axes.linewidth': 1.2,
        'axes.spines.top': False, # Open top for a cleaner look
        'axes.spines.right': False,
        
        # Default props
        'lines.linewidth': 1.5,
    })
    return primary_amber

# --- Helper for the "Glow" Effect ---
def plot_with_glow(ax, x, y, color='#ffb300', label=None):
    """Plots a line with a soft neon glow effect."""
    # 1. The Glow (Thick, transparent)
    ax.plot(x, y, color=color, linewidth=5, alpha=0.15)
    # 2. The Core (Thin, solid)
    ax.plot(x, y, color=color, linewidth=1.5, label=label)

# --- Demo: Digital Sampling ---
primary_color = apply_mojave_theme()

# DSP Data: Analog Signal vs Digital Samples
t_analog = np.linspace(0, 1, 500)
x_analog = np.sin(2 * np.pi * 5 * t_analog) * np.exp(-t_analog)

# Sampling at 20Hz
fs = 20
t_samples = np.arange(0, 1, 1/fs)
x_samples = np.sin(2 * np.pi * 5 * t_samples) * np.exp(-t_samples)

fig, ax = plt.subplots(figsize=(10, 6))

# 1. Plot Analog Reconstruction (With Glow)
plot_with_glow(ax, t_analog, x_analog, label='ANALOG_RECONSTRUCTION')

# 2. Plot Digital Samples (Stem Plot)
# We have to customize stem plots manually to match the theme
markerline, stemlines, baseline = ax.stem(t_samples, x_samples, label='ADC_SAMPLES_20Hz')
plt.setp(stemlines, 'color', '#cc6600', 'linewidth', 1.5)       # Darker amber stems
plt.setp(markerline, 'markerfacecolor', '#ffb300', 'markeredgecolor', '#140c00') # Bright dots
plt.setp(baseline, 'color', '#4d3300', 'linewidth', 1)          # Dim baseline

# Styling
ax.set_title(">> MODULE 4: SAMPLING_THEOREM <<", fontweight='bold', pad=15)
ax.set_xlabel("[ TIME_SECONDS ]")
ax.set_ylabel("[ AMPLITUDE_NORMALIZED ]")

# Add a text annotation for the "Nuclear" vibe
ax.text(0.02, 0.95, "RADIATION: LOW", transform=ax.transAxes, color='#ffb300', fontsize=9)
ax.text(0.02, 0.91, "SNR: 14.2 dB", transform=ax.transAxes, color='#ffb300', fontsize=9)

ax.legend(frameon=False, loc='upper right')

plt.show()