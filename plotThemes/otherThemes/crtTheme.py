import matplotlib.pyplot as plt
from cycler import cycler

def apply_robco_overdrive_theme():
    # --- Color Palette (High Voltage / Overdrive) ---
    crt_bg = '#050a06'          # Darker black-green to increase contrast
    phosphor_dim = '#1f3825'    # Grid lines (darker to make signal pop)
    phosphor_med = '#4a805a'    # Bezel/Borders
    
    # NEW: "Overdrive" Colors
    # We move towards pure neon and high-value tints
    phosphor_neon = '#33ff57'   # Classic "Hacker" bright green
    phosphor_hot  = '#ccffdc'   # Near-white green (core of the beam)
    phosphor_ref  = '#268f45'   # Dimmer reference trace

    text_white = '#e6fff0'      # Slightly brighter text to match

    plt.rcParams.update({
        # Backgrounds (Darker for contrast)
        'figure.facecolor': crt_bg,
        'axes.facecolor': crt_bg,
        'savefig.facecolor': crt_bg,
        
        # Typography
        'font.family': 'monospace',
        'font.size': 11,
        'text.color': text_white,
        'axes.labelcolor': text_white,
        'axes.titlecolor': text_white,
        'xtick.color': text_white,
        'ytick.color': text_white,
        
        # The Scope Grid
        'axes.grid': True,
        'grid.color': phosphor_dim,
        'grid.linestyle': '-', 
        'grid.linewidth': 0.8,
        'grid.alpha': 1.0,
        
        # Borders (Bezel)
        'axes.edgecolor': phosphor_med,
        'axes.linewidth': 1.5,
        'axes.spines.top': True,
        'axes.spines.right': True,
        
        # Data Lines (The "Beam")
        # Increased width to simulate "Bloom" (brightness spread)
        'lines.linewidth': 2.2, 
        
        # Cycle: 
        # 1. Neon (Main Signal)
        # 2. Hot/White (Highlight or Overdriven Signal)
        # 3. Ref (Background Signal)
        'axes.prop_cycle': cycler(color=[
            phosphor_neon, 
            phosphor_hot, 
            phosphor_ref
        ])
    })

# Usage Example
if __name__ == "__main__":
    import numpy as np
    
    # Apply the theme
    apply_robco_overdrive_theme()
    
    # Generate dummy data
    t = np.linspace(0, 10, 500)
    signal = np.sin(t) * np.exp(-0.1 * t)
    noise = np.random.normal(0, 0.05, len(t))
    
    fig, ax = plt.subplots(figsize=(8, 5))
    
    # Plotting standard trace
    ax.plot(t, signal + noise, label="RX_SIGNAL_01")
    
    # Decorating
    ax.set_title(">> SIGNAL INTERCEPT [OVERDRIVE]")
    ax.set_xlabel("TIME (ms)")
    ax.set_ylabel("AMPLITUDE (mV)")
    ax.legend(loc='upper right', frameon=False)
    
    plt.show()