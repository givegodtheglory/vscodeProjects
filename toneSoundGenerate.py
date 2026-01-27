import numpy as np
from scipy.io.wavfile import write

# Settings
fs = 44100       # Sample rate
duration = 3     # Seconds
freq = 500       # Hz

# Generate
t = np.linspace(0, duration, int(fs * duration), endpoint=False)
signal = 0.5 * np.sin(2 * np.pi * 500 * t) +  0.5*np.sin(2 * np.pi * (1200) * t)#0.5 amplitude to avoid clipping

# Save
write("500And1200Hz_tone.wav", fs, (signal * 32767).astype(np.int16))
print("File '500And1000Hz_tone.wav' saved.")