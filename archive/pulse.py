import numpy as np
import matplotlib.pyplot as plt

# --- Parameters ---
A = 1.0        # amplitude
T = 1e-6       # pulse width (seconds)
Fs = 200e6     # sampling rate (Hz)
Tb = 2e-6      # bit period (seconds)
N_bits = 128   # number of bits in train

# --- Helper functions ---
def sinc_pi(z):
    return np.sinc(z)  # numpy's sinc = sin(pi z)/(pi z)

def fft_spectrum(x, Fs, pad_factor=4):
    N_fft = int(2 ** np.ceil(np.log2(len(x) * pad_factor)))
    X = np.fft.fft(x, n=N_fft)
    f = np.fft.fftfreq(N_fft, d=1/Fs)
    Xs = np.fft.fftshift(X)
    fs = np.fft.fftshift(f)
    mag = np.abs(Xs)
    mag_db = 20 * np.log10(mag / np.max(mag))  # normalize to 0 dB
    return fs, mag_db

# --- Case 1: Single pulse ---
N_pulse = int(np.round(T * Fs))
N_signal = 4 * N_pulse
x_single = np.zeros(N_signal)
x_single[:N_pulse] = A

fs_single, mag_single_db = fft_spectrum(x_single, Fs, pad_factor=8)
analytic_env = A * T * np.abs(sinc_pi(fs_single * T))
analytic_env_db = 20 * np.log10(analytic_env / np.max(analytic_env))

plt.figure(figsize=(8,4))
plt.plot(fs_single/1e6, mag_single_db, label='FFT |X(f)| (dB)')
plt.plot(fs_single/1e6, analytic_env_db, '--', label='AT sinc(fT) (dB)')
plt.title('Single Unipolar NRZ Pulse Spectrum (Normalized dB)')
plt.xlabel('Frequency (MHz)')
plt.ylabel('Magnitude (dB)')
plt.legend()
plt.grid(True)

# --- Case 2: Pulse train ---
N_Tb = int(np.round(Tb * Fs))
N_T = int(np.round(T * Fs))
N_signal_train = N_bits * N_Tb

def build_unipolar_nrz(bits):
    x = np.zeros(N_signal_train)
    for k, b in enumerate(bits):
        if b == 1:
            start = k * N_Tb
            x[start:start+N_T] = A
    return x

# Deterministic (all ones)
bits_all1 = np.ones(N_bits, dtype=int)
x_all1 = build_unipolar_nrz(bits_all1)
fs_all1, mag_all1_db = fft_spectrum(x_all1, Fs)

# Random sequence
rng = np.random.default_rng(123)
bits_rand = rng.integers(0, 2, size=N_bits)
x_rand = build_unipolar_nrz(bits_rand)
fs_rand, mag_rand_db = fft_spectrum(x_rand, Fs)

# Analytic envelopes in dB
env_all1 = A * T * np.abs(sinc_pi(fs_all1 * T))
env_all1_db = 20 * np.log10(env_all1 / np.max(env_all1))

env_rand = (A*T)**2 * (sinc_pi(fs_rand*T)**2)
env_rand_db = 20 * np.log10(env_rand / np.max(env_rand))

plt.figure(figsize=(8,4))
plt.plot(fs_all1/1e6, mag_all1_db, label='Deterministic train (dB)')
plt.plot(fs_all1/1e6, env_all1_db, '--', label='Envelope AT sinc(fT) (dB)')
plt.title('Unipolar NRZ Pulse Train Spectrum (All Ones, dB)')
plt.xlabel('Frequency (MHz)')
plt.ylabel('Magnitude (dB)')
plt.legend()
plt.grid(True)

plt.figure(figsize=(8,4))
plt.plot(fs_rand/1e6, mag_rand_db, label='Random train (dB)')
plt.plot(fs_rand/1e6, env_rand_db, '--', label='~(AT)^2 sinc^2 envelope (dB)')
plt.title('Unipolar NRZ Pulse Train Spectrum (Random Bits, dB)')
plt.xlabel('Frequency (MHz)')
plt.ylabel('Magnitude (dB)')
plt.legend()
plt.grid(True)

plt.show()