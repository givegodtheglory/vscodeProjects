import numpy as np
import matplotlib.pyplot as plt
from scipy.fft import fft, fftshift, fftfreq
from helperFunctions import generate_pulse_train

# --- 1. Simulation Parameters ---
n_bits = 1                   # Single pulse
symbolRate = 1               # 1 symbol per second (makes time axis easy to read)
samplingFreqHz = 100         # High enough to see the shapes
alpha = 0.5                  # Rolloff
BT = 0.3                     # Gaussian Bandwidth-Time
span = 6                     # Filter span

# --- 2. Generate Single Pulse Data ---
# We force the bits to be a single '1' to see the impulse response clearly
bits = np.array([1])

# Generate time vector ONCE (since our helper function now guarantees alignment)
_, t = generate_pulse_train('Polar NRZ', bits, symbolRate, alpha, span, BT, samplingFreqHz)

signals = {
    'Unipolar NRZ': generate_pulse_train('Unipolar NRZ', bits,  symbolRate, alpha, span, BT, samplingFreqHz)[0],
    'Polar NRZ': generate_pulse_train('Polar NRZ', bits,  symbolRate, alpha, span, BT, samplingFreqHz)[0],
    'Unipolar RZ': generate_pulse_train('Unipolar RZ', bits, symbolRate, alpha, span, BT, samplingFreqHz)[0],
    'Manchester': generate_pulse_train('Manchester', bits, symbolRate, alpha, span, BT, samplingFreqHz)[0],
    'Raised Cosine': generate_pulse_train('Raised Cosine', bits, symbolRate, alpha, span, BT, samplingFreqHz)[0],
    'Root Raised Cosine': generate_pulse_train('Root Raised Cosine', bits, symbolRate, alpha, span, BT, samplingFreqHz)[0],
    'Gaussian': generate_pulse_train('Gaussian', bits, symbolRate, alpha, span, BT, samplingFreqHz)[0]
}

# --- 3. Compute FFT (Spectrum of Single Pulse) ---
psd_data = {}
N_FFT = 2048 * 8  # Zero padding for smooth frequency plot

for name, sig in signals.items():
    # Compute FFT
    X_f = fft(sig, N_FFT)
    X_mag = np.abs(fftshift(X_f))**2  # Energy Spectral Density
    
    # Generate Freq Axis
    freqs = fftshift(fftfreq(N_FFT, 1/samplingFreqHz))
    
    # Normalize to 0 dB for easy comparison
    peak = np.max(X_mag)
    if peak > 0:
        psd_dB = 10 * np.log10(X_mag / peak)
    else:
        psd_dB = np.zeros_like(X_mag) - 100

    psd_data[name] = {'freqs': freqs, 'psd': psd_dB}

# --- 4. Plotting ---
plt.figure(figsize=(12, 10))

# Time Domain Plot
plt.subplot(2, 1, 1)
offset = 0
for name, sig in signals.items():
    # Safety check to ensure lengths match (they should with your new function)
    plt.plot(t, sig + offset, label=name, linewidth=2) 

plt.title('Baseband Pulse Shapes (Single Bit)')
plt.xlabel('Time (s)')
plt.ylabel('Amplitude (Shifted)')
plt.grid(True, alpha=0.3)
plt.legend(loc='upper right', fontsize='small')

# Frequency Domain Plot
plt.subplot(2, 1, 2)


for name, data in psd_data.items():
    plt.plot(data['freqs'], data['psd'], label=name)

plt.title('Normalized Energy Spectral Density (FFT)')
plt.xlabel('Frequency (Hz)')
plt.ylabel('Magnitude (dB)')
plt.xlim(-5, 5) # Zoom in on the main lobes (since Symbol Rate is 1)
plt.ylim(-60, 5)
plt.grid(True, which='both', linestyle='--', alpha=0.5)
plt.legend()

plt.tight_layout()
plt.show()