import numpy as np
import matplotlib.pyplot as plt
from scipy.fft import fft, fftshift, fftfreq
from helperFunctions import PLASMA_BLUE, RAD_METER_ORANGE, URANIUM_GREEN, generate_pulse_train, auto_organize, plot_flex, CHALK_WHITE, STENCIL_YELLOW, DANGER_RED, AMMO_CRATE_GREEN, ENGRAVED_BLACK
from helperFunctions import get_gaussian_filter_unit_amplitude, get_raised_cosine_filter_unit_amplitude

alpha = 0.35
totalSamplesInSymbol = 100
samplingFreqHz = 100
pulseTimeVector = np.linspace(0, 15, totalSamplesInSymbol, endpoint=True )

signals = {
    'Raised Cosine 1': get_raised_cosine_filter_unit_amplitude(pulseTimeVector-0-4, alpha, samplingFreqHz),
    'Raised Cosine 2': get_raised_cosine_filter_unit_amplitude(pulseTimeVector-2-4, alpha, samplingFreqHz),
    'Raised Cosine 3': get_raised_cosine_filter_unit_amplitude(pulseTimeVector-4-4, alpha, samplingFreqHz),
    'Raised Cosine 4': get_raised_cosine_filter_unit_amplitude(pulseTimeVector-6-4, alpha, samplingFreqHz),
}

pulseTrain =   (
    signals['Raised Cosine 1']
    - signals['Raised Cosine 2']
    + signals['Raised Cosine 3']
    - signals['Raised Cosine 4'])

data_x = [pulseTimeVector]*1
data_y = [
    #signals['Raised Cosine 1'],
    #signals['Raised Cosine 2'],
    #signals['Raised Cosine 3'],
    #signals['Raised Cosine 4'],
    pulseTrain,
    ]


# 3. Define Attributes Lists (Order matches data_x/data_y)
my_titles   = ["RC Pulse Train [1010]"]
my_legends  = ["Pulse"]
my_xtitles  = ["Time (ms)"]
my_ytitles  = ["Voltage (V)"]
my_colors   = [URANIUM_GREEN, ENGRAVED_BLACK , PLASMA_BLUE, DANGER_RED, STENCIL_YELLOW]
my_styles   = ['-', '-', '-', '-', '-']  # <--- Styles: Solid, Dashed, Dotted


# 4. Organize
figures = auto_organize(
    data_x, 
    data_y, 
    layout=[[5]],             # Window 1 has 2 plots, Window 2 has 1 plot
    titles=my_titles,
    xtitles=my_xtitles,
    ytitles=my_ytitles,
    legend_labels=my_legends,
    colors=my_colors,
    linestyles=my_styles,
    legend_locs=[["lower right"]]
)

# 5. Plot

plot_flex(figures,fileName="raisedCosinePlots/RaisedCosinePulseTrain1010_individual5.png")


