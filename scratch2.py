from numpy.fft import fft, fftshift, fftfreq
from numpy import log10, abs
import numpy as np
import matplotlib.pyplot as plt
import plotly.express as px
from helperFunctions import plot, genNRZPulse, genPulseTrain
from scipy.signal import welch, get_window

samplingFrequencyHz = 100000
totalPulseDuration = 4

# Generate Single Pulse 
pulseWidth = 2 #seconds
pulse, pulseTimeVector, pulsefft, pulsefftMagnitude,pulsefftFreqs = genNRZPulse(pulseWidth,totalPulseDuration, samplingFrequencyHz)

# Generate Pulse Train 
data = np.random.randint(0, 2, 1000)
pulsetrainPulseWidth = 0.2;
pulsetrain, pulsetrainTimeVector, pulsetrainfft, pulsetrainfftMagnitude, pulsetrainfftFreqs = genPulseTrain(data, pulsetrainPulseWidth, samplingFrequencyHz)

f, Pxx = welch(
    pulsetrain)

plt.figure()
plt.plot(f, Pxx)


# numSubplots = 5
# plt.figure()
# plt.subplot(numSubplots,1,1)
# plt.plot(pulseTimeVector, pulse)

# plt.subplot(numSubplots,1,2)
# plt.plot(pulseWidth*pulsefftFreqs, 20*log10(pulsefftMagnitude/max(pulsefftMagnitude)))
# plt.ylim(-50,10)

# plt.subplot(numSubplots,1,3)
# plt.plot(pulsetrainTimeVector, pulsetrain)

# plt.subplot(numSubplots,1,4)
# plt.plot(pulsetrainPulseWidth*pulsetrainfftFreqs, abs(pulsetrainfftMagnitude)/max(abs(pulsetrainfftMagnitude)))

# plt.subplot(numSubplots,1,5)
# plt.plot(pulsetrainPulseWidth*pulsetrainfftFreqs, 20*log10(pulsetrainfftMagnitude/max(pulsetrainfftMagnitude)))



# plt.subplot(5,1,4)
# plt.plot(fftPulseTrainFreqs*pulseWidth, np.abs(fftPulseTrain))
# plt.xlim(-1,1)
# plt.subplot(5,1,5)
# plt.plot(fft.fftshift(fftPulseTrainFreqs), fft.fftshift(10*np.log10(np.abs(fftPulseTrain))))
# plt.xlim(-1,1)
# plt.ylim(-30,30)

plt.show()









