import numpy as np
import matplotlib.pyplot as plt
from scipy.fft import fft, fftshift, fftfreq
from helperFunctions import generate_pulse_train, auto_organize, plot_flex, CHALK_WHITE, STENCIL_YELLOW, DANGER_RED


t = np.linspace(0, 1, 100, endpoint=False)
y = np.sin(2*np.pi*1*t)

# --- 3. Compute FFT (Spectrum of Single Pulse) ---
psd_data = {}
N_FFT = 2048 * 8  # Zero padding for smooth frequency plot

data_x = [t]
data_y = [y]

# 3. Define Attributes Lists (Order matches data_x/data_y)
my_titles   = ["Sin Wave"]
my_legends  = ["Sin Wave"]
my_xtitles  = ["Time (ms)"]
my_ytitles  = ["Voltage (V)"]
my_colors   = [CHALK_WHITE]
my_styles   = ['-']  # <--- Styles: Solid, Dashed, Dotted

# 4. Organize
figures = auto_organize(
    data_x, 
    data_y, 
    layout=[[1]],             # Window 1 has 2 plots, Window 2 has 1 plot
    titles=my_titles,
    xtitles=my_xtitles,
    ytitles=my_ytitles,
    legend_labels=my_legends,
    colors=my_colors,
    linestyles=my_styles,
    legend_locs=[[[0.85,0.12]]],
    jupiter_locs=[["lower right"]])

# 5. Plot
plot_flex(figures,fileName="sineWave.png")
