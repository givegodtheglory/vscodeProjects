import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import welch
from helperFunctions import generate_pulse_train

# --- 1. Simulation Parameters ---
n_bits = 600       # Large number of bits for smooth PSD
symbolRate = 200             # Symbols per second
samplingFreqHz = 100000          # Sampling frequency (Hz)

alpha = 0.35         # Rolloff factor for RC and RRC
BT = 0.3             # Bandwidth-Time product for Gaussian pulse
span = 10            # Filter span in symbols

carrierFrequencyHz = 5000
cosineSignalDurationSeconds = 10

# Generate random data
bits = np.random.randint(0, 2, n_bits)
dataPulseTrain, t = generate_pulse_train('Polar NRZ', bits, symbolRate, alpha, span, BT, samplingFreqHz)

# Generate the cosine carrier signal: c(t) = cos(2 * pi * fc * t)
carrier = np.cos(2 * np.pi * carrierFrequencyHz * t)
print(np.mean(carrier))
askSignal = dataPulseTrain*carrier

signals = {
 'Unipolar NRZ': generate_pulse_train('Unipolar NRZ', bits,  symbolRate, alpha, span, BT, samplingFreqHz)[0] * carrier,
 'Polar NRZ': generate_pulse_train('Polar NRZ', bits,  symbolRate, alpha, span, BT, samplingFreqHz)[0] * carrier,
 'Unipolar RZ': generate_pulse_train('Unipolar RZ', bits, symbolRate, alpha, span, BT, samplingFreqHz)[0] * carrier,
 'Manchester': generate_pulse_train('Manchester', bits, symbolRate, alpha, span, BT, samplingFreqHz)[0] * carrier,
 'Raised Cosine': generate_pulse_train('Raised Cosine', bits, symbolRate, alpha, span, BT, samplingFreqHz)[0] * carrier,
 'Root Raised Cosine': generate_pulse_train('Root Raised Cosine', bits, symbolRate, alpha, span, BT, samplingFreqHz)[0] * carrier,
 'Gaussian': generate_pulse_train('Gaussian', bits, symbolRate, alpha, span, BT, samplingFreqHz)[0] * carrier
}

psd_data = {}
for name, sig in signals.items():
 freqs, psd = welch(sig, samplingFreqHz, nperseg=4096, return_onesided='True')
 psd_data[name] = {'freqs': freqs, 'psd': 10 * np.log10(psd)}

plt.figure(figsize=(10, 6))
plt.subplot(2, 1, 1)
offset = 0
for name, sig in signals.items():
 plt.plot(t, sig + offset, label=name)
 offset -= 2.5 # Shift down for visibility
plt.title('ASK Modulated Pulse Shapes in Time Domain (Offset for comparison)')
plt.xlabel('Time (s)')
plt.ylabel('Amplitudes (Shifted)')

#plt.xlim(0, 0.05) # Show first few symbols
plt.grid(True, alpha=0.3)
plt.legend(loc='upper right', fontsize='small')

plt.subplot(2, 1, 2)
for name, data in psd_data.items():
 plt.plot(data['freqs'], data['psd'], label=name)

plt.title('Power Spectral Density Comparison of ASK Signals (Welch Method)')
plt.xlabel('Frequency (Hz)')
plt.ylabel('PSD (dB/Hz)')
plt.xlim(carrierFrequencyHz - 5000, carrierFrequencyHz + 5000) # Show around the carrier frequency
plt.ylim(-100, 5)
plt.grid(True, which='both', linestyle='--', alpha=0.5)
plt.legend()
plt.tight_layout()
plt.show()
