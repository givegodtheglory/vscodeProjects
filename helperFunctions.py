import numpy as np
import matplotlib.pyplot as plt
import plotly.express as px

def plot(xArg, yArg, xAxisTitle=0, yAxisTitle=0, plotTitle=0):
    
    fig = px.line(x=xArg, y=yArg)
    fig.update_layout(template="plotly_dark")
    fig.show()
    
    return 0

def genNRZPulse(pulseWidthArg,totalPulseWidthArg, samplingFrequencyHz = 100):
    
    # Generate pulse
    pulseWidth = pulseWidthArg #seconds
    totalPulseWidth = totalPulseWidthArg #seconds

    numberOfActiveSamples = pulseWidth * samplingFrequencyHz
    numberOfZeroSamples = samplingFrequencyHz*totalPulseWidth - numberOfActiveSamples

    timeVector = np.arange(-totalPulseWidth/2,totalPulseWidth/2, 1/samplingFrequencyHz)

    activePulseSection = np.ones(int(numberOfActiveSamples))
    prefixZeroSection = np.zeros(int(numberOfZeroSamples/2))
    trailingZeroSection = prefixZeroSection

    pulse = np.concatenate((prefixZeroSection, activePulseSection,trailingZeroSection))

    fftPulse = (np.fft.fft(pulse,12*len(pulse)))
    fftPulse = fftPulse/(12*len(pulse))

    fftPulseFreqs = np.fft.fftfreq(len(fftPulse), 1/samplingFrequencyHz)
    fftPulseFreqs = fftPulseFreqs * pulseWidth 

    fmin = -5 / pulseWidth
    fmax =  5 / pulseWidth
    mask = (fftPulseFreqs >= fmin) & (fftPulseFreqs <= fmax)
    fftPulse_trimmed = fftPulse[mask]
    fftPulseFreqs_trimmed = fftPulseFreqs[mask]
    fftPulseFreqs_trimmed /= pulseWidth
    return pulse, timeVector, np.fft.fftshift(fftPulse_trimmed), np.abs(np.fft.fftshift(fftPulse_trimmed)), np.fft.fftshift(fftPulseFreqs_trimmed)

def genPulseTrain(bitSequence, bitDuration, samplingFrequencyHz):
    #Create a pulse train

    samplesPerBit = int(bitDuration * samplingFrequencyHz)

    # Build pulse train by concatenating sections
    pulseSections = []
    for bit in bitSequence:
        if bit == 1:
            pulseSections.append(np.ones(samplesPerBit))
        else:
            pulseSections.append(np.zeros(samplesPerBit))

    pulseTrain = np.concatenate(pulseSections)

    pulseTrainTimeVector = np.arange(len(pulseTrain)) / samplingFrequencyHz

    autoCorrelationPulseTrain = np.correlate(pulseTrain, pulseTrain, mode='full')
    fftPulseTrain = np.fft.fft(autoCorrelationPulseTrain,32*len(autoCorrelationPulseTrain))
    fftPulseTrain = fftPulseTrain / (32*len(autoCorrelationPulseTrain))
    fftPulseTrainFreqs = np.fft.fftfreq(len(fftPulseTrain), 1/samplingFrequencyHz)
    fftPulseTrainFreqs = np.fft.fftshift(fftPulseTrainFreqs)
    fftPulseTrainFreqs *= bitDuration

    fmin = -5 / bitDuration
    fmax =  5 / bitDuration
    mask = (fftPulseTrainFreqs >= fmin) & (fftPulseTrainFreqs <= fmax)
    fftPulseTrain_trimmed = fftPulseTrain[mask]
    fftPulseTrainFreqs_trimmed = fftPulseTrainFreqs[mask]
    fftPulseTrainFreqs_trimmed /= bitDuration
    

    return pulseTrain, pulseTrainTimeVector, np.fft.fftshift(fftPulseTrain_trimmed), np.abs(np.fft.fftshift(fftPulseTrain_trimmed)), fftPulseTrainFreqs_trimmed

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

def generate_pulse_train(pulse_type, bits, bipolar_bits, sps, alpha, span, BT, total_duration_samples=None):
    n_bits = len(bits)
    
    # Determine the length of the pulse train
    if total_duration_samples is None:
        total_samples = n_bits * sps
    else:
        total_samples = total_duration_samples

    # Create a time vector for the generated pulse train
    time_vector = np.arange(total_samples) / sps

    if pulse_type == 'Unipolar NRZ':
        pulse_train = np.repeat(bits, sps)
    elif pulse_type == 'Polar NRZ':
        pulse_train = np.repeat(bipolar_bits, sps)
    elif pulse_type == 'Unipolar RZ':
        rz = np.zeros(n_bits * sps)
        for i, b in enumerate(bits):
            if b == 1:
                rz[i*sps : i*sps + sps//2] = 1
        pulse_train = rz
    elif pulse_type == 'Manchester':
        manchester = np.zeros(n_bits * sps)
        for i, b in enumerate(bits):
            if b == 1:
                manchester[i*sps : i*sps + sps//2] = 1
                manchester[i*sps + sps//2 : (i+1)*sps] = -1
            else: # b == 0
                manchester[i*sps : i*sps + sps//2] = -1
                manchester[i*sps + sps//2 : (i+1)*sps] = 1
        pulse_train = manchester
    elif pulse_type == 'Raised Cosine':
        upsampled = np.zeros(n_bits * sps)
        upsampled[::sps] = bipolar_bits
        pulse_train = np.convolve(upsampled, get_rc_filter(alpha, span, sps), mode='same')
    elif pulse_type == 'Root Raised Cosine':
        upsampled = np.zeros(n_bits * sps)
        upsampled[::sps] = bipolar_bits
        pulse_train = np.convolve(upsampled, get_rrc_filter(alpha, span, sps), mode='same')
    elif pulse_type == 'Gaussian':
        upsampled = np.zeros(n_bits * sps)
        upsampled[::sps] = bipolar_bits
        pulse_train = np.convolve(upsampled, get_gauss_filter(BT, span, sps), mode='same')
    else:
        raise ValueError("Unknown pulse type")

    # Trim or pad the pulse train to the desired total_samples
    if len(pulse_train) > total_samples:
        pulse_train = pulse_train[:total_samples]
    elif len(pulse_train) < total_samples:
        pulse_train = np.pad(pulse_train, (0, total_samples - len(pulse_train)), 'constant')

    return pulse_train, time_vector
