import matplotlib.pyplot as plt
import numpy as np
import matplotlib.font_manager as fm

def apply_robco_scope_theme():
    # --- Color Palette (Monochromatic Green) ---
    # We use shades of the same hue to prevent "vibration"
    crt_bg = '#0d120f'        # Very deep, warm black-green (not pure black)
    phosphor_dim = '#2a4030'  # Grid lines (faint, background)
    phosphor_med = '#5c8a68'  # Secondary data / borders
    phosphor_bright = '#85e0a3' # Main data lines (soft glow, not neon)
    text_white = '#d4edda'    # Pale green-white for high legibility
    
    plt.rcParams.update({
        # Backgrounds
        'figure.facecolor': crt_bg,
        'axes.facecolor': crt_bg,
        'savefig.facecolor': crt_bg,
        
        # Typography (Terminal Style)
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
        'grid.linestyle': '-',    # Solid lines look more like an analog scope
        'grid.linewidth': 0.8,
        'grid.alpha': 1.0,        # Use color for subtlety, not alpha
        
        # Borders (Bezel)
        'axes.edgecolor': phosphor_med,
        'axes.linewidth': 1.5,
        'axes.spines.top': True,
        'axes.spines.right': True,
        
        # Data Lines
        'lines.linewidth': 1.8,
        # Cycle allows for multiple lines without breaking the color theme
        # We use brightness levels instead of different colors
        'axes.prop_cycle': plt.cycler(color=[
            '#85e0a3', # Signal (Bright)
            '#4a7a58', # Reference (Dim)
            '#d4edda'  # Highlight (White-ish)
        ])
    })

# --- Demo: DSP Signal Processing ---
apply_robco_scope_theme()

# Generate a mock DSP signal (AM Modulation)
t = np.linspace(0, 0.1, 1000)
carrier = np.sin(2 * np.pi * 200 * t)
modulator = 1 + 0.5 * np.sin(2 * np.pi * 20 * t)
signal = carrier * modulator

# Add some "thermal noise" for realism
noise = np.random.normal(0, 0.1, len(t))
noisy_signal = signal + noise

fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(10, 8))
plt.subplots_adjust(hspace=0.4)

# Plot 1: Time Domain (Scope View)
ax1.plot(t * 1000, noisy_signal, label='RX_INPUT_RAW', linewidth=1.2)
ax1.set_title(">> SIGNAL_ACQUISITION: ANTENNA_A <<", fontweight='bold', pad=10)
ax1.set_xlabel("TIME (ms)")
ax1.set_ylabel("AMPLITUDE (V)")
ax1.set_xlim(0, 40)
ax1.legend(loc='upper right', frameon=False, fontsize=10)

# Plot 2: Frequency Domain (FFT View)
freqs = np.fft.rfftfreq(len(t), t[1]-t[0])
mag = np.abs(np.fft.rfft(noisy_signal))
mag_db = 20 * np.log10(mag + 1e-6) # Convert to dB

ax2.plot(freqs, mag_db, color='#d4edda', linewidth=1.5, label='PSD_ESTIMATE')
ax2.set_title(">> SPECTRAL_ANALYSIS: FFT_CORE <<", fontweight='bold', pad=10)
ax2.set_xlabel("FREQUENCY (Hz)")
ax2.set_ylabel("POWER (dB)")
ax2.set_xlim(0, 500)
ax2.set_ylim(-20, 60)

# Annotation: Bandwidth Marker
ax2.axvspan(150, 250, color='#2a4030', alpha=0.5, label='PASSBAND')
ax2.text(200, 50, "CARRIER\n200 Hz", ha='center', va='center', color='#85e0a3', fontsize=9)

plt.show()