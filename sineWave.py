import numpy as np
import matplotlib.pyplot as plt
from scipy.fft import fft, fftshift, fftfreq, rfft, rfftfreq
from helperFunctions import generate_pulse_train, auto_organize, plot_flex, CHALK_WHITE, STENCIL_YELLOW, DANGER_RED
from scipy.signal import welch
import random
import string

# --- 1. Generate Data ---
# Time Domain
t = np.linspace(0, 1, 2000, endpoint=True)
y = np.sin(2*np.pi*10*t) # Changed freq to 10Hz so it looks better in time domain

# Frequency Domain
fftSin = rfft(y)
dt = t[1]-t[0]
fftSamplingFreq = 1/dt
fftFreqs = rfftfreq(len(y), d=1/fftSamplingFreq)

# --- 2. Process Frequency Data (Split Tone vs Noise) ---
tone_index_mask = np.isclose(fftFreqs, 10.0, atol=0.01) # Matching the 10Hz signal

# Dataset A: Noise (Everything EXCEPT the tone)
x_noise = fftFreqs[~tone_index_mask]
y_noise = np.abs(fftSin)[~tone_index_mask]

# Dataset B: Tone (ONLY the tone)
x_tone = fftFreqs[tone_index_mask]
y_tone = np.abs(fftSin)[tone_index_mask]

# --- 3. Organize Data for Plotter ---
# We now have 3 distinct traces to plot:
# 1. Time Domain Signal
# 2. Frequency Noise Floor
# 3. Frequency Discrete Tone
all_x = [t, x_noise, x_tone]
all_y = [y, y_noise, y_tone]

# Define Colors for the 3 traces
# Time = White, Noise = White, Tone = Red
my_colors = [CHALK_WHITE, CHALK_WHITE, CHALK_WHITE]

# --- 4. Configure Layout ---
figures = auto_organize(
    all_x, 
    all_y, 
    
    # LAYOUT: Window 1 has [Subplot 1 (1 trace), Subplot 2 (2 traces)]
    layout=[[1, 2]], 
    
    titles=["Time Domain", "Frequency Spectrum"],
    xtitles=["Time (s)", "Frequency (Hz)"],
    ytitles=["Amplitude (V)", "Magnitude"],
    
    legend_labels=["Signal", "Noise Floor", "Discrete Tone"],
    
    # PLOT TYPES:
    # Subplot 1: ["line"]
    # Subplot 2: ["line", "stem"]
    plot_types=[[ ["line"], ["line", "stem"] ]],
    
    colors=my_colors,
    
    # Optional: Zoom in on the frequency plot to see the split better
    xlims=[[None, (0, 20)]] 
)

# 5. Plot
randString = ''.join(random.choices(string.ascii_letters + string.digits, k=16))
plot_flex(figures, fileName=randString + "_CombinedPlot.png")