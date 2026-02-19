import numpy as np
import matplotlib.pyplot as plt
from scipy.fft import fft, fftshift, fftfreq
from helperFunctions import generate_pulse_train, auto_organize, plot_flex, CHALK_WHITE, STENCIL_YELLOW, DANGER_RED
from scipy.signal import welch


# --- 1. THEME DEFINITION (Fat Man) ---
AMMO_CRATE_GREEN = '#2e3b2b'
STENCIL_YELLOW = '#f0c808'
CHALK_WHITE = '#e0e0e0'
DANGER_RED = '#ff3333'
ENGRAVED_BLACK = '#1a2118'

# --- EXPANDED FATMAN PALETTE ---
# Special Highlighting
PLASMA_BLUE       = '#6699cc'  # Soft glow blue
URANIUM_GREEN     = '#39ff14'  # "Radioactive" bright neon green (Use sparingly)


#bits = np.array([1,0,1])
bits = np.random.randint(0, 2, 6)
samplingFreq, baud = 100000, 200

# 1. Create Reference NRZ (This generates the master time vector)
nrz, t_master = generate_pulse_train('Unipolar NRZ', bits, baud, samplingFreq, 
                                     prefix_symbols=2, suffix_symbols=2)

signals = {
    'Unipolar NRZ': generate_pulse_train(
        'Unipolar NRZ', bits, baud, samplingFreq, 
        prefix_symbols=2, suffix_symbols=2, external_t=t_master)[0],
    
    'Polar NRZ': generate_pulse_train(
        'Polar NRZ', bits, baud, samplingFreq, 
        prefix_symbols=2, suffix_symbols=2, external_t=t_master)[0],
    
    'Unipolar RZ': generate_pulse_train(
        'Unipolar RZ', bits, baud, samplingFreq, 
        prefix_symbols=2, suffix_symbols=2, external_t=t_master)[0],
    
    'Manchester': generate_pulse_train(
        'Manchester', bits, baud, samplingFreq, 
        prefix_symbols=2, suffix_symbols=2, external_t=t_master)[0],
    
    'Raised Cosine': generate_pulse_train(
        'Raised Cosine', bits, baud, samplingFreq, 
        alpha=0.1, prefix_symbols=2, suffix_symbols=2, external_t=t_master)[0],
    
    'Root Raised Cosine': generate_pulse_train('Root Raised Cosine', bits, baud, samplingFreq, 
        alpha=0.1, prefix_symbols=2, suffix_symbols=2, external_t=t_master)[0],
    
    'Gaussian': generate_pulse_train('Gaussian', bits, baud, samplingFreq, BT=0.3, prefix_symbols=2, suffix_symbols=2, external_t=t_master)[0]
}

# --- 3. Compute FFT (Spectrum of Single Pulse) ---
# carrierFrequencyHz = 0
# carrier = 1*np.cos(2 * np.pi * carrierFrequencyHz * t_master)
# y = signals["Unipolar NRZ"]*carrier
# fftMagPulse = np.abs(fft(y)*1/samplingFreqHz) #normalized fft
# fftMagPulse = fftshift(fftMagPulse)
# pulsePSD = fftMagPulse**2
# freqs = fftfreq(len(y), 1/samplingFreqHz)
# freqs = fftshift(freqs)


def get_psd(sig, fs):
    f, pxx = welch(sig, fs, nperseg=2022, return_onesided=False, detrend=False)
    return np.fft.fftshift(f), 10 * np.log10(np.fft.fftshift(pxx))

psd_data = {}
for name, sig in signals.items():
 freqs, psd = get_psd(sig, samplingFreq)
 psd_data[name] = {'freqs': freqs, 'psd': psd}



data_x = [
   t_master,
   t_master,
   t_master,
   t_master,
   t_master,
   psd_data['Unipolar NRZ']['freqs'],
   psd_data['Unipolar NRZ']['freqs'],
   psd_data['Unipolar NRZ']['freqs'],
   psd_data['Unipolar NRZ']['freqs'],
   psd_data['Unipolar NRZ']['freqs'],
   ]

data_y = [
   signals['Unipolar NRZ'],
   signals['Polar NRZ'],
   signals['Root Raised Cosine'],
   signals['Raised Cosine'],
   signals['Gaussian'],
   psd_data['Unipolar NRZ']['psd'],
   psd_data['Polar NRZ']['psd'],
   psd_data['Root Raised Cosine']['psd'],
   psd_data['Raised Cosine']['psd'],
   psd_data['Gaussian']['psd']
]



# 3. Define Attributes Lists (Order matches data_x/data_y)
#my_titles   = ["Unipolar NRZ Pulse Time Domain", "Unipolar NRZ Pulse PSD"]
my_titles   = ["Pulsetrain Comparison"]

my_legends  = [
    "Unipolar NRZ Pulse Train", 
    "Polar NRZ Pulse Train", 
    "Root Raised Cosine Pulse Train", 
    "Raised Cosine Pulse Train", 
    "Gaussian Pulse Train"
    "Unipolar NRZ Pulse Train PSD", 
    "Polar NRZ Pulse Train PSD", 
    "Root Raised Cosine Pulse Train PSD", 
    "Raised Cosine Pulse Train PSD", 
    "Gaussian Pulse Train PSD"]

#my_xtitles  = ["Time (ms)", "Frequency (Hz)"]
my_xtitles  = ["Frequency (Hz)"]
my_ytitles  = ["Voltage (V)", "Magnitude (dB)"]
my_colors   = [URANIUM_GREEN, DANGER_RED,  STENCIL_YELLOW]
my_styles   = ['-']  # <--- Styles: Solid, Dashed, Dotted


# 4. Organize
figures = auto_organize(
    data_x, 
    data_y, 
    layout=[[4,4]],             
    titles=my_titles,
    xtitles=my_xtitles,
    xlims=[(),
           [(-10000,10000)]],
    ylims=[[(),
            (-200,1)]],
    ytitles=my_ytitles,
    legend_labels=my_legends,
    colors=my_colors,
    linestyles=my_styles       # <--- Passing the styles list
)

# 5. Plot
plot_flex(figures, fileName="trash/unipolarNRZPulsePSDShowingSideBands3.png")

