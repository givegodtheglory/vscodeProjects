import numpy as np
import matplotlib.pyplot as plt
from scipy.fft import fft, fftfreq, fftshift

# Parameters
fs = 10000  # Sampling frequency
T = 1       # Duration in seconds
t = np.linspace(0, T, int(fs*T), endpoint=False)

# 1. Baseband pulse (Gaussian)
pulse_width = 0.01
pulse = np.exp(-((t - T/2)**2) / (2 * pulse_width**2))

# FFT of baseband pulse
pulse_fft = fftshift(fft(pulse))
freqs = fftshift(fftfreq(len(t), 1/fs))

# Plot baseband pulse
plt.figure(figsize=(12, 4))
plt.subplot(1, 2, 1)
plt.plot(t, pulse)
plt.title("Baseband Pulse (Time Domain)")
plt.xlabel("Time [s]")

plt.subplot(1, 2, 2)
plt.plot(freqs, np.abs(pulse_fft))
plt.title("Baseband Pulse (Frequency Domain)")
plt.xlabel("Frequency [Hz]")
plt.tight_layout()
plt.show()

# 2. Pulse sequence
pulse_spacing = 0.1
sequence = np.zeros_like(t)
for i in range(0, len(t), int(pulse_spacing * fs)):
    sequence[i:i+len(pulse)//100] += pulse[:len(pulse)//100]

# FFT of pulse sequence
seq_fft = fftshift(fft(sequence))

# Plot pulse sequence
plt.figure(figsize=(12, 4))
plt.subplot(1, 2, 1)
plt.plot(t, sequence)
plt.title("Pulse Sequence (Time Domain)")
plt.xlabel("Time [s]")

plt.subplot(1, 2, 2)
plt.plot(freqs, np.abs(seq_fft))
plt.title("Pulse Sequence (Frequency Domain)")
plt.xlabel("Frequency [Hz]")
plt.tight_layout()
plt.show()

# 3. FSK modulation
f0 = 100  # Frequency for bit 0
f1 = 300  # Frequency for bit 1
bit_duration = 0.1
bits = np.random.randint(0, 2, int(T / bit_duration))

fsk_signal = np.zeros_like(t)
for i, bit in enumerate(bits):
    f = f1 if bit else f0
    idx_start = int(i * bit_duration * fs)
    idx_end = int((i + 1) * bit_duration * fs)
    fsk_signal[idx_start:idx_end] = np.cos(2 * np.pi * f * t[idx_start:idx_end]) * pulse[idx_start:idx_end]

# FFT of FSK signal
fsk_fft = fftshift(fft(fsk_signal))

# Plot FSK signal
plt.figure(figsize=(12, 4))
plt.subplot(1, 2, 1)
plt.plot(t, fsk_signal)
plt.title("FSK Modulated Signal (Time Domain)")
plt.xlabel("Time [s]")

plt.subplot(1, 2, 2)
plt.plot(freqs, np.abs(fsk_fft))
plt.title("FSK Modulated Signal (Frequency Domain)")
plt.xlabel("Frequency [Hz]")
plt.tight_layout()
plt.show()
