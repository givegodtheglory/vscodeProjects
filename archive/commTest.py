import numpy as np
import matplotlib.pyplot as plt

# Generate baseband data (example)
data = np.array([0,1,1,0,0])
num_bits = len(data)

# Parameters
bit_rate = 10   # bits per second
f0 = 1000       # Frequency for binary '0' (Hz)
f1 = 5000       # Frequency for binary '1' (Hz)
sample_rate = 100000  # Samples per second
duration_per_bit = 0.2 # seconds

# Time vector for one bit
samples_per_bit = 4*int(sample_rate * duration_per_bit)
timeVectorForOneBit = np.linspace(0, duration_per_bit, samples_per_bit, endpoint=False)

# Generate FSK signal and baseband waveform (unipolar NRZ)
fsk_signal = np.array([])
baseband_signal = np.array([])

for bit in data:
    freq = f1 if bit == 1 else f0
    fsk_segment = np.sin(2 * np.pi * freq * timeVectorForOneBit)
    fsk_signal = np.concatenate((fsk_signal, fsk_segment))
    baseband_segment = np.ones_like(timeVectorForOneBit) * bit
    baseband_signal = np.concatenate((baseband_signal, baseband_segment))

# Time vector for entire signal
t = np.linspace(0, duration_per_bit * num_bits, num_bits * samples_per_bit, endpoint=False)

# Define carrier frequency for upconversion
f_c = 3000  # Hz (choose a frequency higher than your baseband bandwidth)

# Generate cosine carrier
carrier = np.cos(2 * np.pi * f_c * t)

# Increase FFT resolution by zero-padding
desired_fft_length = 8 * len(baseband_signal)

# FFT of NRZ pulse (no carrier, just the pulse train)
fft_pulse = np.fft.fft(baseband_signal, n=desired_fft_length)
freqs_pulse = np.fft.fftfreq(desired_fft_length, d=1/sample_rate)
positive_freqs_pulse = freqs_pulse[freqs_pulse >= 0]
magnitude_pulse = np.real(fft_pulse[freqs_pulse >= 0])

# FFT of baseband signal (after upconversion)
fft_baseband = np.fft.fft(baseband_signal * carrier, n=desired_fft_length)
freqs_baseband = np.fft.fftfreq(desired_fft_length, d=1/sample_rate)
positive_freqs_baseband = freqs_baseband[freqs_baseband >= 0]
magnitude_baseband = np.real(fft_baseband[freqs_baseband >= 0])

# FFT of FSK signal
fft_fsk = np.fft.fft(fsk_signal, n=desired_fft_length)
freqs_fsk = np.fft.fftfreq(desired_fft_length, d=1/sample_rate)
positive_freqs_fsk = freqs_fsk[freqs_fsk >= 0]
magnitude_fsk = np.real(fft_fsk[freqs_fsk >= 0])

# Plot signals and FFTs
plt.figure(figsize=(12, 8))

# Time-domain NRZ pulse
plt.subplot(5, 1, 1)
plt.plot(t, baseband_signal, drawstyle='steps-post')
plt.title("Unipolar NRZ Pulse (Time Domain)")
plt.xlabel("Time (s)")
plt.ylabel("Amplitude")
plt.ylim(-0.5, 1.5)
plt.grid(True)

# FFT of NRZ pulse
plt.subplot(5, 1, 2)
plt.plot(positive_freqs_pulse, magnitude_pulse)
plt.title("FFT of Unipolar NRZ Pulse")
plt.xlabel("Frequency (Hz)")
plt.ylabel("Magnitude")
plt.xlim(-20, 20)
plt.grid(True)

# FFT of baseband (upconverted)
plt.subplot(5, 1, 3)
plt.plot(positive_freqs_baseband, magnitude_baseband)
plt.title("FFT of Baseband Signal (Upconverted)")
plt.xlabel("Frequency (Hz)")
plt.ylabel("Magnitude")
plt.xlim(0, 6000)
plt.grid(True)

# FFT of FSK
plt.subplot(5, 1, 4)
plt.plot(positive_freqs_fsk, magnitude_fsk)
plt.title("FFT of FSK Signal")
plt.xlabel("Frequency (Hz)")
plt.ylabel("Magnitude")
plt.xlim(0, 6000)
plt.grid(True)

# Time-domain FSK
plt.subplot(5, 1, 5)
plt.plot(t, fsk_signal)
plt.title("FSK Modulated Signal (Time Domain)")
plt.xlabel("Time (s)")
plt.ylabel("Amplitude")
plt.grid(True)

plt.tight_layout()
plt.show()