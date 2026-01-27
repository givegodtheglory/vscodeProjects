import numpy as np
import matplotlib.pyplot as plt
from scipy.fft import fft, fftshift, fftfreq
from helperFunctions import PLASMA_BLUE, RAD_METER_ORANGE, URANIUM_GREEN, generate_pulse_train, auto_organize, plot_flex, CHALK_WHITE, STENCIL_YELLOW, DANGER_RED, AMMO_CRATE_GREEN, ENGRAVED_BLACK


# --- Parameters ---
bits = np.array([1,1]) # Two bits to see overlap
symbolRate = 1000
samplingFreqHz = 10000
alpha = 0
span = 6  # Large span to see tails clearly
BT = 0.3
pulse_type_to_test = 'Raised Cosine' # or 'Root Raised Cosine'

# --- Generate Data in Debug Mode ---
# This returns the summed train (pt), time (t), and list of individual pulses (traces)
pt, t, debug_traces = generate_pulse_train(
    pulse_type_to_test, 
    bits, 
    symbolRate, 
    alpha, 
    span, 
    BT, 
    samplingFreqHz, 
    debug_mode=True
)


# --- Prepare Data for Your Custom Plotting Functions ---

# 1. Initialize lists with the main summed output trace
data_x = [t]
data_y = [pt]
my_legends = ["Summed Output (Red)"]
my_colors = [DANGER_RED, CHALK_WHITE, URANIUM_GREEN]
my_styles = ['-'] # Solid line for sum

# 2. Append the individual bit traces (e.g., as white dashed lines)
for i, trace in enumerate(debug_traces):
    data_x.append(t)
    data_y.append(trace)
    my_legends.append(f"Individual Bit {i} Pulse") 
    my_styles.append('--') # Dashed lines for components

# 3. Define Titles
my_titles = [f"{pulse_type_to_test} Overlap Debug (Alpha={alpha}, Span={span})"]
my_xtitles = ["Time (s)"]
my_ytitles = ["Normalized Voltage (V)"]


# 4. Organize (Assuming auto_organize takes lists of lists for multiple traces on one plot)
# We are putting ALL traces onto a single plot ([1])
figures = auto_organize(
    data_x, 
    data_y, 
    layout=[[3]],             
    titles=my_titles,
    xtitles=my_xtitles,
    ytitles=my_ytitles,
    legend_labels=my_legends,
    colors=my_colors,
    linestyles=my_styles,
    # legend_locs=[[(0.7,0.7)]] # Adjust location if needed
)

# 5. Plot
randomString = np.random.randint(100)
fileName = str(randomString) + f"Debug_{pulse_type_to_test.replace(' ','')}.png"
print(f"Generating plot: {fileName}")
plot_flex(figures, fileName=fileName) # Uncomment to run with your library