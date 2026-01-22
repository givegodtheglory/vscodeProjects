import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import welch
from helperFunctions import generate_pulse_train
# --- 1. Simulation Parameters ---
numberOfSymbols = 1000 # Large number of bits for smooth PSD
symbolRate = 10      #Symbols per second 
samplingFreqHz = 10001

alpha = 0.35         # Rolloff factor for RC and RRC
BT = 0.3             # Bandwidth-Time product for Gaussian pulse
span = 10            # Filter span in symbols

carrierFrequencyHz = 1000

# Generate random data
bits = np.random.randint(0, 2, numberOfSymbols)
bipolar_bits = np.where(bits == 1, 1, -1)
pskPhaseOffsetRadians= np.pi/4

pulse_types = [
 'Unipolar NRZ', 'Polar NRZ', 'Unipolar RZ', 'Manchester',
 'Raised Cosine', 'Root Raised Cosine', 'Gaussian'
]

psk_signals = {}
psd_data = {}

for pulse_type in pulse_types:
 # Generate the data pulse
 dataPulseTrain, t = generate_pulse_train(pulse_type, bits, symbolRate, alpha, span, BT, samplingFreqHz)

 # Generate the time varying cosine angle argument
 modulatedPhase = (dataPulseTrain * pskPhaseOffsetRadians)
 modulatedAngleArgument = 2 * np.pi * carrierFrequencyHz * t + modulatedPhase
 pskSignal = np.cos(modulatedAngleArgument)

 psk_signals[pulse_type] = pskSignal
 freqs, psd = welch(pskSignal, samplingFreqHz, nperseg=4096)
 psd_data[pulse_type] = {'freqs': freqs, 'psd': 10 * np.log10(psd)}

plt.figure(figsize=(12, 8))

plt.subplot(2, 1, 1)
offset = 0
for name, sig in psk_signals.items():
 plt.plot(t, sig + offset, label=name)
 offset -= 2.5 # Shift down for visibility
plt.xlim(0, 5*1/symbolRate) # Show first few symbols
plt.title('PSK Signals in Time Domain (Offset for comparison)')
plt.legend(loc='upper right', fontsize='small')

plt.subplot(2, 1, 2)
for name, data in psd_data.items():
 plt.plot(data['freqs'], data['psd'], label=name)
plt.title('Power Spectral Density Comparison of PSK Signals (Welch Method)')
plt.xlim(carrierFrequencyHz - 500, carrierFrequencyHz + 500) # Show around the carrier frequency
plt.ylim(-100, 5)
plt.legend()
plt.show()