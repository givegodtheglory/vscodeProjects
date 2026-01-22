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

#Generate the data pulse
dataPulseTrain, t = generate_pulse_train('Polar NRZ', bits, symbolRate, alpha, span, BT, samplingFreqHz)
print(bits[0:5])
# Generate the time varying cosine angle argument
pskPhaseOffsetRadians= np.pi/4
modulatedPhase = (dataPulseTrain * pskPhaseOffsetRadians)
modulatedAngleArgument = 2 * np.pi * carrierFrequencyHz * t + modulatedPhase
fskSignal = np.cos(modulatedAngleArgument)
freqs, psd = welch(fskSignal, samplingFreqHz, nperseg=4096)

plt.figure(figsize=(10, 6))
plt.subplot(3, 1, 1)
plt.plot(t, fskSignal, label='FSK Signal')
plt.xlim(0, 5*1/symbolRate) # Show first few symbols
plt.title('PSK Signal in Time Domain')
plt.subplot(3, 1, 2)
plt.plot(t, dataPulseTrain, label='Data Pulse Train')
plt.xlim(0, 5*1/symbolRate) # Show first few symbols
plt.subplot(3, 1, 3)
plt.plot(freqs, np.log10(psd), label='Data Pulse Train')
plt.show()