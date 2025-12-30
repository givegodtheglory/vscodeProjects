import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import welch
from helperFunctions import get_gauss_filter, get_rc_filter, get_rrc_filter, generate_pulse_train

# --- 1. Simulation Parameters ---
n_bits = 10000       # Large number of bits for smooth PSD
samplesPerSymbol = 32             # Samples per symbol (oversampling factor)

#totalNumberOfBits = n_bits * sps

samplingFrequencyHz = 1600            # Sampling frequency (Hz)
bitRate = samplingFrequencyHz / samplesPerSymbol        # Bit rate (bps)
alpha = 0.35         # Rolloff factor for RC and RRC
BT = 0.3             # Bandwidth-Time product for Gaussian pulse
span = 10            # Filter span in symbols

# Generate random data
bits = np.random.randint(0, 2, n_bits)
bipolar_bits = np.where(bits == 1, 1, -1)

# Generate signals and compute PSDs

signals = {
 'Unipolar NRZ': generate_pulse_train('Unipolar NRZ', bits, bipolar_bits, samplesPerSymbol, alpha, span, BT),
 'Polar NRZ': generate_pulse_train('Polar NRZ', bits, bipolar_bits, samplesPerSymbol, alpha, span, BT),
 'Unipolar RZ': generate_pulse_train('Unipolar RZ', bits, bipolar_bits, samplesPerSymbol, alpha, span, BT),
 'Manchester': generate_pulse_train('Manchester', bits, bipolar_bits, samplesPerSymbol, alpha, span, BT),
 'Raised Cosine': generate_pulse_train('Raised Cosine', bits, bipolar_bits, samplesPerSymbol, alpha, span, BT),
 'Root Raised Cosine': generate_pulse_train('Root Raised Cosine', bits, bipolar_bits, samplesPerSymbol, alpha, span, BT),
 'Gaussian': generate_pulse_train('Gaussian', bits, bipolar_bits, samplesPerSymbol, alpha, span, BT)
}

psd_data = {}
for name, sig in signals.items():
    # sig is now a tuple (pulse_train, time_vector)
    freqs, psd = welch(sig[0], samplingFrequencyHz, nperseg=2048)
    psd_data[name] = {'freqs': freqs / bitRate, 'psd': 10 * np.log10(psd)}

plt.figure()
# Time Domain (Subplot 1)
plt.subplot(2, 1, 1)
t_plot = np.arange(8 * samplesPerSymbol) / samplingFrequencyHz # Show 8 bits
offset = 0
for name, (sig, time_vec) in signals.items(): # Unpack the tuple here
    # Use the time_vec from the generate_pulse_train function
    plt.plot(time_vec[:8*samplesPerSymbol], sig[:8*samplesPerSymbol] + offset, label=name)
    offset -= 2.5 # Shift down for visibility
plt.title('Pulse Shapes in Time Domain (Offset for comparison)')
plt.xlabel('Time (s)')
plt.ylabel('Amplitudes (Shifted)')
plt.grid(True, alpha=0.3)
plt.legend(loc='upper right', fontsize='small')

# Frequency Domain (Subplot 2)
plt.subplot(2, 1, 2)
for name, data in psd_data.items():
    plt.plot(data['freqs'], data['psd'], label=name)

plt.title('Power Spectral Density Comparison (Welch Method)')
plt.xlabel('Normalized Frequency ($f / R_b$)')
plt.ylabel('PSD (dB/Hz)')
plt.xlim(0, 4)  # Show first few lobes
plt.ylim(-70, 5)
plt.grid(True, which='both', linestyle='--', alpha=0.5)
plt.legend()
plt.tight_layout()
plt.show()