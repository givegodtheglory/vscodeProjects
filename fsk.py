import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import welch
from helperFunctions import get_gauss_filter, get_rc_filter, get_rrc_filter, generate_pulse_train

# --- 1. Simulation Parameters ---
numberOfSymbols = 10 # Large number of bits for smooth PSD
symbolRate = 10      #Symbols per second 
samplingFreqHz = 100

samplesPerSymbol = samplingFreqHz/symbolRate     # Samples per symbol (oversampling factor)
bitRate = samplingFreqHz / samplesPerSymbol        # Bit rate (bps)

alpha = 0.35         # Rolloff factor for RC and RRC
BT = 0.3             # Bandwidth-Time product for Gaussian pulse
span = 10            # Filter span in symbols

carrierFrequencyHz = 1000


# Generate random data
bits = np.random.randint(0, 2, numberOfSymbols)
bipolar_bits = np.where(bits == 1, 1, -1)

#Generate the data pulse
dataPulseTrain, t = generate_pulse_train('Polar NRZ', bits, bipolar_bits, samplesPerSymbol, alpha, span, BT, samplingFreqHz, symbolRate)
print(bits[0:5])
# Generate the time varying cosine angle argument
fskFreqOffsetHz = 500
modulatedFrequency = carrierFrequencyHz + (dataPulseTrain * fskFreqOffsetHz)
angleArgument = 2 * np.pi * modulatedFrequency * t

fskSignal = np.cos(angleArgument)


plt.figure()
plt.plot(t, dataPulseTrain)
plt.xlim(0, 5*1/symbolRate) # Show first 5 symbols
plt.show()

# plt.figure(figsize=(10, 6))
# plt.subplot(2, 1, 1)
# offset = 0
# for name, sig in signals.items():
#  plt.plot(t, sig + offset, label=name)
#  offset -= 2.5 # Shift down for visibility
# plt.title('ASK Modulated Pulse Shapes in Time Domain (Offset for comparison)')
# plt.xlabel('Time (s)')
# plt.ylabel('Amplitudes (Shifted)')

# plt.grid(True, alpha=0.3)
# plt.legend(loc='upper right', fontsize='small')

# plt.subplot(2, 1, 2)
# for name, data in psd_data.items():
#  plt.plot(data['freqs'], data['psd'], label=name)

# plt.title('Power Spectral Density Comparison of ASK Signals (Welch Method)')
# plt.xlabel('Frequency (Hz)')
# plt.ylabel('PSD (dB/Hz)')
# plt.xlim(carrierFrequencyHz - 5000, carrierFrequencyHz + 5000) # Show around the carrier frequency
# plt.ylim(-100, 5)
# plt.grid(True, which='both', linestyle='--', alpha=0.5)
# plt.legend()
# plt.tight_layout()
# plt.show()
