import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import welch
from helperFunctions import generate_pulse_train, auto_organize, plot_flex, AMMO_CRATE_GREEN, STENCIL_YELLOW, CHALK_WHITE, DANGER_RED


n_bits = 2000
symbolRate = 100
samplingFreqHz = 10000
carrierFrequencyHz = 0
alpha = 0.35
BT = 0.3
span = 10

bits = np.random.randint(0, 2, n_bits)

# --- Signal Generation ---
signals = {}
signal_names = ['Unipolar NRZ', 'Polar NRZ', 'Unipolar RZ', 'Manchester', 
                'Raised Cosine', 'Root Raised Cosine', 'Gaussian']

# Reference time needed for carrier generation
_, t, _, _ = generate_pulse_train('Unipolar NRZ', bits, symbolRate, alpha, span, BT, samplingFreqHz, return_pulse_shape=True)
carrier = np.cos(2 * np.pi * carrierFrequencyHz * t)

for name in signal_names:
    basebandData, _, _, _ = generate_pulse_train(name, bits, symbolRate, alpha, span, BT, samplingFreqHz, return_pulse_shape=True)
    signals[name] = basebandData * carrier

# --- PSD Calculation ---
psd_x, psd_y = [], []
for name in signal_names:
    f, p = welch(signals[name], samplingFreqHz, nperseg=2048, return_onesided=False)
    psd_x.append(f)
    psd_y.append(10 * np.log10(p + 1e-12))

# --- Plot Prep ---
plot_colors = [CHALK_WHITE, DANGER_RED, STENCIL_YELLOW, '#00e5ff', '#ff9900', '#39ff14', '#c3b091']

figures = auto_organize(
    psd_x, 
    psd_y,
    layout=[[len(signals)]], # 1 Window, 1 Subplot, 7 Traces
    titles=["Power Spectral Density Comparison"],
    xtitles=["Frequency (Hz)"],
    ytitles=["PSD (dB/Hz)"],
    legend_labels=signal_names,
    colors=plot_colors,
    plot_types=["line"],
    # Zoom around carrier
    xlims=[[
        (carrierFrequencyHz - 1000, carrierFrequencyHz + 1000)
    ]],
    legend_locs=[["upper right"]],
    logo_locs=[["lower right"]]
)

plot_flex(figures, base_figsize=(12, 6), fileName="PSD_Comparison_Only2.png")