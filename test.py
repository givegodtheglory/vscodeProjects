import numpy as np
import matplotlib.pyplot as plt
from scipy.fft import fft, fftshift, fftfreq, rfft, rfftfreq
from helperFunctions import generate_pulse_train, auto_organize, plot_flex, CHALK_WHITE, STENCIL_YELLOW, DANGER_RED
from scipy.signal import welch
import random
import string


t = np.linspace(0, 1, 1000, endpoint=True)
y = np.sin(2*np.pi*1*t)

fftSin = abs(rfft(y))
dt = t[1]-t[0]
fftSamplingFreq = 1/dt
fftFreqs = rfftfreq(len(y),d=1/fftSamplingFreq)

plt.figure(figsize=(10, 6))
plt.stem(fftFreqs, fftSin, label='Data Pulse Train',)
plt.show()