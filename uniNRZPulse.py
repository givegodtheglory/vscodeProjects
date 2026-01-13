import numpy as np
import matplotlib.pyplot as plt
from scipy.fft import fft, fftshift, fftfreq
from helperFunctions import generate_pulse_train, auto_organize, plot_flex, CHALK_WHITE, STENCIL_YELLOW, DANGER_RED


# --- 1. Simulation Parameters ---
n_bits = 1                   # Single pulse
symbolRate = 1               # 1 symbol per second (makes time axis easy to read)
samplingFreqHz = 100         # High enough to see the shapes
alpha = 0.5                  # Rolloff
BT = 0.3                     # Gaussian Bandwidth-Time
span = 6                     # Filter span

# --- 2. Generate Single Pulse Data ---
# We force the bits to be a single '1' to see the impulse response clearly
#bits = np.array([1])
bits = np.array([0, 1,0])

# Generate time vector ONCE (since our helper function now guarantees alignment)
_, t = generate_pulse_train('Polar NRZ', bits, symbolRate, alpha, span, BT, samplingFreqHz)

signals = {
    'Unipolar NRZ': generate_pulse_train('Unipolar NRZ', bits,  symbolRate, alpha, span, BT, samplingFreqHz)[0],
    # 'Polar NRZ': generate_pulse_train('Polar NRZ', bits,  symbolRate, alpha, span, BT, samplingFreqHz)[0],
    # 'Unipolar RZ': generate_pulse_train('Unipolar RZ', bits, symbolRate, alpha, span, BT, samplingFreqHz)[0],
    # 'Manchester': generate_pulse_train('Manchester', bits, symbolRate, alpha, span, BT, samplingFreqHz)[0],
    # 'Raised Cosine': generate_pulse_train('Raised Cosine', bits, symbolRate, alpha, span, BT, samplingFreqHz)[0],
    # 'Root Raised Cosine': generate_pulse_train('Root Raised Cosine', bits, symbolRate, alpha, span, BT, samplingFreqHz)[0],
    # 'Gaussian': generate_pulse_train('Gaussian', bits, symbolRate, alpha, span, BT, samplingFreqHz)[0]
}

# --- 3. Compute FFT (Spectrum of Single Pulse) ---
psd_data = {}
N_FFT = 2048 * 8  # Zero padding for smooth frequency plot
y = signals["Unipolar NRZ"]
data_x = [t]
data_y = [y]

# 3. Define Attributes Lists (Order matches data_x/data_y)
my_titles   = ["Basic Pulse", "Harmonic Distortion", "Thermal Runaway"]
my_legends  = ["OSC_ALPHA", "OSC_BETA", "TEMP_CRITICAL"]
my_xtitles  = ["Time (ms)", "Time (ms)", "Time (s)"]
my_ytitles  = ["Voltage (V)", "Voltage (V)", "Temp (C)"]
my_colors   = [CHALK_WHITE, STENCIL_YELLOW, DANGER_RED]
my_styles   = ['-', '--', ':']  # <--- Styles: Solid, Dashed, Dotted


# 4. Organize
figures = auto_organize(
    data_x, 
    data_y, 
    layout=[1],             # Window 1 has 2 plots, Window 2 has 1 plot
    titles=my_titles,
    xtitles=my_xtitles,
    ytitles=my_ytitles,
    legend_labels=my_legends,
    colors=my_colors,
    linestyles=my_styles       # <--- Passing the styles list
)

# 5. Plot
plot_flex(figures)
