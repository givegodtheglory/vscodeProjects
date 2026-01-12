import matplotlib.pyplot as plt
import matplotlib.patheffects as pe
from cycler import cycler
import numpy as np

# ==========================================
# ☢️  ROBCO TERMINAL THEME: "FIELD SCANNER" VARIATION ☢️
# ==========================================

THEME_COLORS = {
    'bg_green': '#2e3b2b',      # Same Ammo crate matte green
    'text_yellow': '#ffcc00',   # Same Stencil paint yellow
    'outline_dark': '#1a2118',  # Same Deep dark gray/black
    'trace_white': '#ffffff',   # Same Primary signal
    'trace_red': '#ff4d4d'      # Same Critical signal
}

def set_scanner_theme():
    """
    Applies the military theme with a 'Digital/Scope' feel.
    """
    c = THEME_COLORS
    plt.rcParams.update({
        # --- Backgrounds ---
        'figure.facecolor': c['bg_green'],
        'axes.facecolor':   c['bg_green'],
        'savefig.facecolor': c['bg_green'],
        
        # --- Typography ---
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
        
        # --- Borders & Grid (VARIATION: DOTTED GRID) ---
        'axes.edgecolor': c['text_yellow'],
        'axes.linewidth': 2.5,
        'axes.spines.top': True,
        'axes.spines.right': True,
        'axes.grid': True,
        'grid.color': c['outline_dark'],
        'grid.linestyle': ':',  # <--- CHANGED: Dotted grid for precision look
        'grid.linewidth': 2,    # Slightly thicker dots
        'grid.alpha': 0.7,
        
        # --- Line Defaults ---
        'lines.linewidth': 3.5, # Slightly thinner lines to contrast with the fill
        'axes.prop_cycle': cycler(color=[c['trace_white'], c['trace_red'], c['text_yellow']])
    })

def apply_theme_effects(ax):
    """
    Applies the standard heavy outlines.
    """
    c = THEME_COLORS
    
    # 1. Effects
    line_effect = [pe.Stroke(linewidth=6, foreground=c['outline_dark']), pe.Normal()]
    text_effect = [pe.Stroke(linewidth=3, foreground=c['outline_dark']), pe.Normal()]
    # The 'projecting' capstyle makes the border corners sharp and connected
    border_effect = [pe.Stroke(linewidth=8, foreground=c['outline_dark'], capstyle='projecting'), pe.Normal()]

    # 2. Apply to Borders
    for spine in ax.spines.values():
        spine.set_capstyle('projecting')
        spine.set_path_effects(border_effect)

    # 3. Apply to Lines
    for line in ax.get_lines():
        line.set_path_effects(line_effect)
        
    # 4. Apply to Text
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
    # 1. Set global theme
    set_scanner_theme()

    # Data
    x = np.linspace(0, 10, 40) # Fewer points to emphasize the 'steps'
    y1 = np.sin(x) * 5 + 10
    y2 = np.cos(x * 1.5) * 3 + 5
    
    fig, ax = plt.subplots(figsize=(10, 6))
    
    # 2. Plot Data (VARIATION: Stepped Lines + Fill)
    # Plot standard lines first (using steps-mid for digital look)
    l1, = ax.plot(x, y1, label='SIG_INPUT_A', drawstyle='steps-mid')
    l2, = ax.plot(x, y2, label='SIG_INPUT_B', drawstyle='steps-mid')
    
    # Add the "HUD Fill" under the lines using the same colors
    # We use step='mid' to match the line drawstyle
    ax.fill_between(x, y1, alpha=0.15, color=l1.get_color(), step='mid')
    ax.fill_between(x, y2, alpha=0.15, color=l2.get_color(), step='mid')

    ax.set_title(">> SPECTRUM ANALYZER: M-42 <<", pad=20)
    ax.set_xlabel("FREQUENCY (MHz)")
    ax.set_ylabel("GAIN (dB)")
    
    # 3. Apply Effects (Outlines)
    apply_theme_effects(ax)

    # Legend
    leg = ax.legend(loc='upper right', frameon=True)
    leg.get_frame().set_facecolor(THEME_COLORS['outline_dark'])
    leg.get_frame().set_edgecolor(THEME_COLORS['text_yellow'])
    leg.get_frame().set_linewidth(2.5)
    leg.get_frame().set_path_effects([
        pe.Stroke(linewidth=6, foreground=THEME_COLORS['outline_dark']),
        pe.Normal()
    ])

    plt.show()