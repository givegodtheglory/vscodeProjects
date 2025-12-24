import numpy as np
import matplotlib.pyplot as plt

# Generate pulse
#Baseband data
data = np.array([1])
pulseWidth = 0.2 #seconds
totalPulseWidth = 4 #seconds
trailingZeroWidth = (totalPulseWidth-pulseWidth) / 2
samplingRate = 10000 #Hz

numberOfActiveSamples = pulseWidth * samplingRate
numberOfZeroSamples = samplingRate*totalPulseWidth - numberOfActiveSamples

# Add trailing zeros before and after data
totalPulseTimeVector = np.linspace(0, totalPulseWidth, totalPulseWidth*samplingRate)

activePulseSection = np.ones(int(numberOfActiveSamples))
prefixZeroSection = np.zeros(int(numberOfZeroSamples/2))
trailingZeroSection = prefixZeroSection

pulse = np.concatenate((prefixZeroSection,activePulseSection,trailingZeroSection))
print(pulse)
print(len(pulse))

plt.figure(figsize=(12, 8))

plt.subplot(2, 1, 1)
plt.plot(totalPulseTimeVector,pulse)

fftPulse = np.fft.fftshift(np.fft.fft(pulse,100000))

plt.subplot(2, 1, 2)
plt.plot(fftPulse)
#plt.xlim(4000, 6000)
plt.show()