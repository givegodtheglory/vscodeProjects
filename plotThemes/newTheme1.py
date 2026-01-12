import matplotlib.pyplot as plt
from cycler import cycler

def apply_robco_terminal_amber():
    # --- Color Palette (Monochrome Amber) ---
    # High contrast, sharp, "burnt-in" look
    term_bg = '#1a1400'         # Very dark warm brown/black
    term_fg = '#ffb000'         # Classic Amber Phosphor
    term_dim = '#593e00'        # Dimmed amber for grids
    term_alert = '#ff5500'      # Secondary "Alert" Orange
    
    plt.rcParams.update({
        # Backgrounds (High Contrast)
        'figure.facecolor': term_bg,
        'axes.facecolor': term_bg,
        'savefig.facecolor': term_bg,
        
        # Typography (Strictly Digital)
        'font.family': 'monospace',
        'font.size': 12,            # Slightly larger, blockier text
        'text.color': term_fg,
        'axes.labelcolor': term_fg,
        'axes.titlecolor': term_fg,
        'xtick.color': term_fg,
        'ytick.color': term_fg,
        
        # The "ASCII" Grid
        # We use dotted lines to mimic text characters like " . . . "
        'axes.grid': True,
        'grid.color': term_dim,
        'grid.linestyle': ':',      # Dotted grid feels more "digital/text"
        'grid.linewidth': 1.0,
        'grid.alpha': 1.0,
        
        # Borders (Thick Terminal Window)
        'axes.edgecolor': term_fg,
        'axes.linewidth': 2.0,      # Thicker, distinct border
        'axes.spines.top': True,
        'axes.spines.right': True,
        
        # Data Traces (Sharp & Flat)
        'lines.linewidth': 1.5,     # Thinner, sharper lines (no bloom)
        
        # Cycle: 
        # 1. Main Amber 
        # 2. Alert Orange (for thresholds/errors)
        # 3. Dim Amber (history/old data)
        'axes.prop_cycle': cycler(color=[
            '#ffb000',  # Main Amber
            '#ff5500',  # Alert/Error
            '#996a00'   # Dim/History
        ]),
        
        # Ticks (Inward facing, like a ruler)
        'xtick.direction': 'in',
        'ytick.direction': 'in',
        'xtick.major.size': 6,
        'ytick.major.size': 6,
    })

# Usage Example
if __name__ == "__main__":
    import numpy as np
    
    apply_robco_terminal_amber()
    
    x = np.linspace(0, 10, 20)  # Fewer points for a "jagged" digital look
    y1 = np.sin(x)
    y2 = np.cos(x) * 0.5
    
    fig, ax = plt.subplots(figsize=(8, 5))
    
    # Using 'step' plot often looks more "computer terminal" than standard plot
    ax.step(x, y1, where='mid', label='DATA_STREAM_A')
    ax.step(x, y2, where='mid', label='BUFFER_READ_B')
    
    ax.set_title("> SYSTEM DIAGNOSTIC (VT-320)")
    ax.set_xlabel("BLOCK_INDEX")
    ax.set_ylabel("VALUE_HEX")
    ax.legend(loc='lower left', frameon=True, facecolor='#1a1400', edgecolor='#ffb000')
    
    plt.show()