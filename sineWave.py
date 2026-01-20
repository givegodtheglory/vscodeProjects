import numpy as np
import matplotlib.pyplot as plt
from scipy.fft import fft, fftshift, fftfreq, rfft, rfftfreq
from helperFunctions import generate_pulse_train, auto_organize, plot_flex, CHALK_WHITE, STENCIL_YELLOW, DANGER_RED, KHAKI_SAND
from scipy.signal import welch
import random
import string

# --- 1. Generate Data ---
# Time Domain: Sum of two sine waves (10 Hz and 4 Hz)
t = np.linspace(0, 1, 2000, endpoint=True)
y = np.sin(2*np.pi*10*t) + np.sin(2*np.pi*4*t)



# Frequency Domain
fftSin = rfft(y)
dt = t[1]-t[0]
fftSamplingFreq = 1/dt
fftFreqs = rfftfreq(len(y), d=1/fftSamplingFreq)

# --- 2. Process Frequency Data (Split Tones vs Noise) ---
# [FIXED] Create a mask that finds BOTH 10 Hz and 4 Hz
mask_10 = np.isclose(fftFreqs, 10.0, atol=0.01)
mask_4  = np.isclose(fftFreqs, 4.0,  atol=0.01)

# Combine them with OR (|)
tone_index_mask = mask_10 | mask_4 

# Dataset A: Noise (Everything EXCEPT the tones)
x_noise = fftFreqs[~tone_index_mask]
y_noise = np.abs(fftSin)[~tone_index_mask]

# Dataset B: Tones (ONLY 4 Hz and 10 Hz)
x_tone = fftFreqs[tone_index_mask]
y_tone = np.abs(fftSin)[tone_index_mask]

# --- 3. Organize Data for Plotter ---
# 1. Time Domain Signal
# 2. Frequency Noise Floor (Line)
# 3. Frequency Discrete Tones (Stem)
all_x = [t, x_noise, x_tone]
all_y = [y, y_noise, y_tone]

# Colors: Time=White, Noise=White, Tones=Red
my_colors = [CHALK_WHITE, CHALK_WHITE, CHALK_WHITE]

# --- 4. Configure Layout ---
figures = auto_organize(
    all_x, 
    all_y, 
    
    # Window 1: [Top Subplot (1 trace), Bottom Subplot (2 traces)]
    layout=[[1, 2]],
    
    titles=["Time Domain", "Frequency Spectrum"],
    xtitles=["Time (s)", "Frequency (Hz)"],
    ytitles=["Amplitude (V)", "Magnitude"],
    
    legend_labels=["Signal", "Noise Floor", "Discrete Tones"],
    
    # Top: Line | Bottom: Line + Stem
    plot_types=[[ ["line"], ["line", "stem"] ]],
    
    colors=my_colors,
    
    # Zoom to 0-20Hz to see the 4Hz and 10Hz clearly
    xlims=[[None, (0, 20)]],
    
    # [FIXED] Updated legend structure to match layout (1 win -> 2 subplots)
    legend_locs=[["upper right", "upper right"]],
    logo_locs=[["lower right", "lower right"]] 
)

# 5. Plot
plot_flex(figures, fileName="sineWaveMultiTone.png")