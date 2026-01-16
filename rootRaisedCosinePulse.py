import numpy as np
import matplotlib.pyplot as plt
from scipy.fft import fft, fftshift, fftfreq
from helperFunctions import PLASMA_BLUE, RAD_METER_ORANGE, URANIUM_GREEN, generate_pulse_train, auto_organize, plot_flex, CHALK_WHITE, STENCIL_YELLOW, DANGER_RED, AMMO_CRATE_GREEN, ENGRAVED_BLACK


# --- 1. Simulation Parameters ---
n_bits = 1                   # Single pulse
symbolRate = 1               # 1 symbol per second (makes time axis easy to read)
samplingFreqHz = 100         # High enough to see the shapes
alpha = 0.2                  # Rolloff
BT = 0.3                     # Gaussian Bandwidth-Time
span = 6                     # Filter span

# --- 2. Generate Single Pulse Data ---
# We force the bits to be a single '1' to see the impulse response clearly
#bits = np.array([1])
bits = np.array([1])

# Generate time vector ONCE (since our helper function now guarantees alignment)
# NEW (Fixed)
#pt, t, shape_y, shape_t = generate_pulse_train('Root Raised Cosine', bits, symbolRate, alpha, span, BT, samplingFreqHz, return_pulse_shape=True)


# --- 3. Compute FFT (Spectrum of Single Pulse) ---
psd_data = {}
N_FFT = 2048 * 8  # Zero padding for smooth frequency plot

pt, t, rcZeroAlpha, shape_t = generate_pulse_train('Root Raised Cosine', bits, symbolRate, 0, span, BT, samplingFreqHz, return_pulse_shape=True)
pt, t, rcPointThreeAlpha, shape_t = generate_pulse_train('Root Raised Cosine', bits, symbolRate, 0.3, span, BT, samplingFreqHz, return_pulse_shape=True)
pt, t, rcPointEightAlpha, shape_t = generate_pulse_train('Root Raised Cosine', bits, symbolRate, 0.8, span, BT, samplingFreqHz, return_pulse_shape=True)
pt, t, rcOneAlpha, shape_t = generate_pulse_train('Root Raised Cosine', bits, symbolRate, 1, span, BT, samplingFreqHz, return_pulse_shape=True)



data_x = [shape_t+3, shape_t+3, shape_t+3, shape_t+3]
data_y = [10*rcZeroAlpha, 10*rcPointThreeAlpha, 10*rcPointEightAlpha, 10*rcOneAlpha]

# 3. Define Attributes Lists (Order matches data_x/data_y)
my_titles   = ["Root Raised Cosine (RC) Pulse"]
my_legends  = ["Alpha = 0", "Alpha = 0.3", "Alpha = 0.8", "Alpha = 1"]
my_xtitles  = ["Time (ms)"]
my_ytitles  = ["Voltage (V)"]
my_colors   = [URANIUM_GREEN, RAD_METER_ORANGE , PLASMA_BLUE, DANGER_RED]
my_styles   = ['-']  # <--- Styles: Solid, Dashed, Dotted


# 4. Organize
figures = auto_organize(
    data_x, 
    data_y, 
    layout=[[4]],             # Window 1 has 2 plots, Window 2 has 1 plot
    titles=my_titles,
    xtitles=my_xtitles,
    ytitles=my_ytitles,
    legend_labels=my_legends,
    colors=my_colors,
    linestyles=my_styles       # <--- Passing the styles list
)

# 5. Plot
plot_flex(figures,fileName="RootRaisedCosinePulseComparison.png")
