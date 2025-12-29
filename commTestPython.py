import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import welch

# --- 1. Simulation Parameters ---
n_bits = 10000       # Large number of bits for smooth PSD
sps = 32             # Samples per symbol (oversampling factor)
fs = 1600            # Sampling frequency (Hz)
rb = fs / sps        # Bit rate (bps)
alpha = 0.35         # Rolloff factor for RC and RRC
BT = 0.3             # Bandwidth-Time product for Gaussian pulse
span = 10            # Filter span in symbols

# Generate random data
bits = np.random.randint(0, 2, n_bits)
bipolar_bits = np.where(bits == 1, 1, -1)

# --- 2. Filter Design Functions ---
def get_rrc_filter(alpha, span, sps):
    t = np.arange(-span*sps//2, span*sps//2 + 1) / sps
    h = np.zeros(len(t))
    for i, val in enumerate(t):
        if val == 0:
            h[i] = 1 - alpha + 4*alpha/np.pi
        elif alpha != 0 and abs(val) == 1/(4*alpha):
            h[i] = alpha/np.sqrt(2) * ((1+2/np.pi)*np.sin(np.pi/(4*alpha)) + (1-2/np.pi)*np.cos(np.pi/(4*alpha)))
        else:
            num = np.sin(np.pi*val*(1-alpha)) + 4*alpha*val*np.cos(np.pi*val*(1+alpha))
            den = np.pi*val*(1-(4*alpha*val)**2)
            h[i] = num/den
    return h / np.sqrt(np.sum(h**2))

def get_rc_filter(alpha, span, sps):
    t = np.arange(-span*sps//2, span*sps//2 + 1) / sps
    # Handle the divide-by-zero cases in the RC formula
    h = np.sinc(t) * np.cos(np.pi*alpha*t) / (1 - (2*alpha*t)**2 + 1e-10)
    return h / np.sum(h)

def get_gauss_filter(BT, span, sps):
    t = np.arange(-span*sps//2, span*sps//2 + 1) / sps
    sigma = np.sqrt(np.log(2)) / (2 * np.pi * BT)
    h = np.exp(-t**2 / (2 * sigma**2))
    return h / np.sum(h)

# --- 3. Signal Generation ---

# Square Pulses
unipolar_nrz = np.repeat(bits, sps)
polar_nrz = np.repeat(bipolar_bits, sps)

# Unipolar RZ (Return to Zero)
rz = np.zeros(n_bits * sps)
for i, b in enumerate(bits):
    if b == 1:
        rz[i*sps : i*sps + sps//2] = 1

# Manchester
manchester = np.zeros(n_bits * sps)
for i, b in enumerate(bits):
    if b == 1:
        manchester[i*sps : i*sps + sps//2] = 1
        manchester[i*sps + sps//2 : (i+1)*sps] = -1
    else:
        manchester[i*sps : i*sps + sps//2] = -1
        manchester[i*sps + sps//2 : (i+1)*sps] = 1

# Shaped Pulses (via Convolution)
upsampled = np.zeros(n_bits * sps)
upsampled[::sps] = bipolar_bits  # Pulse train

rc_sig = np.convolve(upsampled, get_rc_filter(alpha, span, sps), mode='same')
rrc_sig = np.convolve(upsampled, get_rrc_filter(alpha, span, sps), mode='same')
gauss_sig = np.convolve(upsampled, get_gauss_filter(BT, span, sps), mode='same')

# --- 4. Plotting ---
signals = {
    'Unipolar NRZ': unipolar_nrz,
    'Polar NRZ': polar_nrz,
    'Unipolar RZ': rz,
    'Manchester': manchester,
    'Raised Cosine': rc_sig,
    'Root Raised Cosine': rrc_sig,
    'Gaussian': gauss_sig
}

plt.figure(figsize=(14, 10))

# Time Domain (Subplot 1)
plt.subplot(2, 1, 1)
t_plot = np.arange(8 * sps) / fs # Show 8 bits
offset = 0
for name, sig in signals.items():
    plt.plot(t_plot, sig[:8*sps] + offset, label=name)
    offset -= 2.5 # Shift down for visibility

plt.title('Pulse Shapes in Time Domain (Offset for comparison)')
plt.xlabel('Time (s)')
plt.ylabel('Amplitudes (Shifted)')
plt.grid(True, alpha=0.3)
plt.legend(loc='upper right', fontsize='small')

# Frequency Domain (Subplot 2)
plt.subplot(2, 1, 2)
for name, sig in signals.items():
    # pwelch calculation
    freqs, psd = welch(sig, fs, nperseg=2048)
    
    # Normalize frequency by bit rate (f/Rb)
    # Convert to dB
    plt.plot(freqs/rb, 10 * np.log10(psd), label=name)

plt.title('Power Spectral Density Comparison (Welch Method)')
plt.xlabel('Normalized Frequency ($f / R_b$)')
plt.ylabel('PSD (dB/Hz)')
plt.xlim(0, 4)  # Show first few lobes
plt.ylim(-70, 5)
plt.grid(True, which='both', linestyle='--', alpha=0.5)
plt.legend()

plt.tight_layout()
plt.show()