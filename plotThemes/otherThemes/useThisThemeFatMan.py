import matplotlib.pyplot as plt
import matplotlib.patheffects as pe
import matplotlib.patches as patches  # <--- NEW IMPORT
from cycler import cycler
import numpy as np

# ==========================================
# ☢️  ROBCO TERMINAL THEME: "FAT MAN" (HIGH CONTRAST) ☢️
# ==========================================

THEME_COLORS = {
    'bg_green': '#2e3b2b',      
    'text_yellow': '#ffcc00',   
    'outline_dark': '#1a2118',  
    'trace_white': '#ffffff',   
    'trace_red': '#ff4d4d'      
}

def set_fatman_theme():
    c = THEME_COLORS
    plt.rcParams.update({
        'figure.facecolor': c['bg_green'],
        'axes.facecolor':   c['bg_green'],
        'savefig.facecolor': c['bg_green'],
        'font.family': 'monospace',
        'font.size': 11,
        'font.weight': 'bold',
        'axes.labelweight': 'bold',
        'axes.titleweight': 'bold',
        'text.color': c['text_yellow'],
        'axes.labelcolor': c['text_yellow'],
        'axes.titlecolor': c['text_yellow'],
        'xtick.color': c['text_yellow'],
        'ytick.color': c['text_yellow'],
        # We turn off the default spine styling here because we will replace them manually
        'axes.linewidth': 0, 
        'axes.grid': True,
        'grid.color': c['outline_dark'],
        'grid.linestyle': '-',
        'grid.linewidth': 1.5,
        'grid.alpha': 0.6,
        'lines.linewidth': 4.5,
        'axes.prop_cycle': cycler(color=[c['trace_white'], c['trace_red'], c['text_yellow']])
    })

def apply_theme_effects(ax):
    """
    Applies high-contrast outlines to Lines, Text, and creates a CUSTOM BORDER box.
    """
    c = THEME_COLORS
    
    # --- 1. Define Effects ---
    line_effect = [pe.Stroke(linewidth=7, foreground=c['outline_dark']), pe.Normal()]
    text_effect = [pe.Stroke(linewidth=3, foreground=c['outline_dark']), pe.Normal()]
    
    # Effect for the Box: Thicker black outline
    border_effect = [
        pe.Stroke(linewidth=8, foreground=c['outline_dark'], joinstyle='miter'),
        pe.Normal()
    ]

    # --- 2. NEW: Replace Spines with a Single Rectangle ---
    # First, hide the default 4 separate spines
    for spine in ax.spines.values():
        spine.set_visible(False)

    # Create a single Rectangle patch that covers the axes area
    # transform=ax.transAxes means (0,0) is bottom-left, (1,1) is top-right
    rect = patches.Rectangle(
        (0, 0), 1, 1, 
        transform=ax.transAxes, 
        linewidth=2.5, 
        edgecolor=c['text_yellow'], 
        facecolor='none', # Transparent inside
        zorder=100        # Make sure it sits on top of the grid
    )
    
    # Apply the outline effect to this single rectangle
    rect.set_path_effects(border_effect)
    
    # Add the rectangle to the plot 
    ax.add_patch(rect)
    # Ensure the border isn't clipped by the figure edge
    rect.set_clip_on(False)

    # --- 3. Apply to Data Lines ---
    for line in ax.get_lines():
        line.set_path_effects(line_effect)
        
    # --- 4. Apply to Text ---
    text_targets = [ax.title, ax.xaxis.label, ax.yaxis.label]
    text_targets.extend(ax.get_xticklabels())
    text_targets.extend(ax.get_yticklabels())
    
    for txt_obj in text_targets:
        txt_obj.set_path_effects(text_effect)
        txt_obj.set_clip_on(False) 

# ==========================================
# 📋 USAGE EXAMPLE
# ==========================================
if __name__ == "__main__":
    set_fatman_theme()

    x = np.linspace(0, 10, 100)
    y1 = np.sin(x) * 5 + 10
    y2 = np.cos(x * 1.5) * 3 + 5
    
    fig, ax = plt.subplots(figsize=(10, 6))
    
    ax.plot(x, y1, label='PRIMARY_COIL_V')
    ax.plot(x, y2, label='TEMP_INJECTOR_C')
    
    ax.set_title(">> FIELD DIAGNOSTIC: M-42 UNIT <<", pad=20)
    ax.set_xlabel("TIME DOMAIN (ms)")
    ax.set_ylabel("AMPLITUDE (kV)")
    
    # Apply Effects LAST
    apply_theme_effects(ax)

    # Legend styling
    leg = ax.legend(loc='upper right', frameon=True)
    leg.get_frame().set_facecolor(THEME_COLORS['outline_dark'])
    leg.get_frame().set_edgecolor(THEME_COLORS['text_yellow'])
    leg.get_frame().set_linewidth(2.5)
    
    leg.get_frame().set_path_effects([
        pe.Stroke(linewidth=6, foreground=THEME_COLORS['outline_dark']),
        pe.Normal()
    ])

    plt.show()