import numpy as np
import matplotlib.pyplot as plt
import plotly.express as px
from cycler import cycler
import matplotlib.patheffects as pe

# --- 1. THEME DEFINITION (Fat Man) ---
AMMO_CRATE_GREEN = '#2e3b2b'
STENCIL_YELLOW = '#f0c808'
CHALK_WHITE = '#e0e0e0'
DANGER_RED = '#ff3333'
ENGRAVED_BLACK = '#1a2118'

def apply_fatman_theme():
    """Activates the M-42 Fat Man visual specification."""
    plt.rcParams.update({
        'figure.facecolor': AMMO_CRATE_GREEN,
        'axes.facecolor': AMMO_CRATE_GREEN,
        'savefig.facecolor': AMMO_CRATE_GREEN,
        'font.family': 'monospace',
        'font.weight': 'bold',
        'font.size': 10,
        'text.color': STENCIL_YELLOW,
        'axes.labelcolor': STENCIL_YELLOW,
        'axes.titlecolor': STENCIL_YELLOW,
        'xtick.color': STENCIL_YELLOW,
        'ytick.color': STENCIL_YELLOW,
        'axes.grid': True,
        'grid.color': ENGRAVED_BLACK,
        'grid.linestyle': '-',
        'grid.linewidth': 1.5,
        'grid.alpha': 0.6,
        'axes.edgecolor': STENCIL_YELLOW,
        'axes.linewidth': 2.5,
        'axes.spines.top': True,
        'axes.spines.right': True,
        'lines.linewidth': 3.0,
        # Default cycle if no specific color is provided
        'axes.prop_cycle': cycler(color=[CHALK_WHITE, DANGER_RED, STENCIL_YELLOW])
    })

# --- 2. THE ORGANIZER ---
def auto_organize(xs, ys, layout, 
                  titles=None,         # Subplot Titles (Top of graph)
                  xtitles=None,        # X-Axis Labels
                  ytitles=None,        # Y-Axis Labels
                  legend_labels=None,  # Trace Names in Legend
                  colors=None,         # Specific colors per trace
                  linestyles=None,     # Line styles (e.g., '--', ':', '-')
                  **kwargs):           # Global fallbacks
    """
    Organizes data lists into the plot structure.
    All list arguments must match the order of the data in xs/ys.
    """
    structure = []
    idx = 0
    
    for count in layout:
        fig_list = []
        for _ in range(count):
            if idx < len(xs):
                d = {'x': xs[idx], 'y': ys[idx]}
                
                # --- Map Lists to Individual Plots ---
                if titles and idx < len(titles): d['title'] = titles[idx]
                if xtitles and idx < len(xtitles): d['xlabel'] = xtitles[idx]
                if ytitles and idx < len(ytitles): d['ylabel'] = ytitles[idx]
                if legend_labels and idx < len(legend_labels): d['legend_label'] = legend_labels[idx]
                if colors and idx < len(colors): d['color'] = colors[idx]
                if linestyles and idx < len(linestyles): d['linestyle'] = linestyles[idx]
                
                # Apply global defaults for anything missing
                for k, v in kwargs.items():
                    if k not in d: d[k] = v
                        
                fig_list.append(d)
                idx += 1
        structure.append(fig_list)
    return structure

# --- 3. THE PLOTTER ---
def plot_flex(figures_data, base_figsize=(10, 5), show=True, fileName="iNeedAFileName.png"):
    """
    Renders the figures. 
    Returns a list of tuples: [(Figure, [Axes]), ...]
    """
    apply_fatman_theme()
    created_figs = []
    
    for subplots_list in figures_data:
        n = len(subplots_list)
        # Create figure with dynamic height based on N subplots
        fig, axes = plt.subplots(n, 1, figsize=(base_figsize[0], base_figsize[1] * n))
        
        # Ensure axes is always a list
        if n == 1: axes = [axes]
        
        for ax, data in zip(axes, subplots_list):
            # --- PLOT THE DATA ---
            ax.plot(data['x'], data['y'], 
                    label=data.get('legend_label'),
                    color=data.get('color'),          # Uses specific color if provided
                    linestyle=data.get('linestyle', '-') # Uses specific style if provided
            )
            
            # --- APPLY LABELS (Uppercased) ---
            if data.get('title'): ax.set_title(f">> {data['title']} <<", fontweight='bold', fontsize=13, pad=20)
            if data.get('xlabel'): ax.set_xlabel(data['xlabel'], fontweight='bold', fontsize=12)
            if data.get('ylabel'): ax.set_ylabel(data['ylabel'], fontweight='bold', fontsize=12, labelpad=10)

            # --- LEGEND ---
            if data.get('legend_label'):
                leg = ax.legend(frameon=True, loc='center right')
                frame = leg.get_frame()
                frame.set_facecolor(ENGRAVED_BLACK)
                frame.set_edgecolor(STENCIL_YELLOW)

            # --- BRANDING ---
            ax.text(0.84, 0.1, "FATMAN INDUSTRIES", transform=ax.transAxes, 
                    fontsize=9, color=AMMO_CRATE_GREEN, fontweight='bold',
                    verticalalignment='top',
                    bbox=dict(facecolor=STENCIL_YELLOW, edgecolor=STENCIL_YELLOW, boxstyle='square,pad=0.2'))

        fig.tight_layout()
        created_figs.append((fig, axes))
        plt.savefig(fileName, dpi=600)

    if show:
        plt.show()
    return created_figs


def plot(xArg, yArg, xAxisTitle=0, yAxisTitle=0, plotTitle=0):
    
    fig = px.line(x=xArg, y=yArg)
    fig.update_layout(template="plotly_dark")
    fig.show()
    
    return 0

def genNRZPulse(pulseWidthArg,totalPulseWidthArg, samplingFrequencyHz = 100):
    
    # Generate pulse
    pulseWidth = pulseWidthArg #seconds
    totalPulseWidth = totalPulseWidthArg #seconds

    numberOfActiveSamples = int(pulseWidth * samplingFrequencyHz)
    totalSamples = int(totalPulseWidth * samplingFrequencyHz)
    numberOfZeroSamples = totalSamples - numberOfActiveSamples

    activePulseSection = np.ones(numberOfActiveSamples)
    prefixZeroSection = np.zeros(int(numberOfZeroSamples/2))
    trailingZeroSection = np.zeros(numberOfZeroSamples - len(prefixZeroSection))

    pulse = np.concatenate((prefixZeroSection, activePulseSection,trailingZeroSection))
    timeVector = np.arange(len(pulse)) / samplingFrequencyHz - totalPulseWidth/2

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
        elif alpha != 0 and np.isclose(abs(val), 1/(4*alpha)):
            h[i] = alpha/np.sqrt(2) * ((1+2/np.pi)*np.sin(np.pi/(4*alpha)) + (1-2/np.pi)*np.cos(np.pi/(4*alpha)))
        else:
            num = np.sin(np.pi*val*(1-alpha)) + 4*alpha*val*np.cos(np.pi*val*(1+alpha))
            den = np.pi*val*(1-(4*alpha*val)**2)
            h[i] = num/den
    return h / np.sqrt(np.sum(h**2))

def get_rc_filter(alpha, span, sps):
    t = np.arange(-span*sps//2, span*sps//2 + 1) / sps
    
    with np.errstate(divide='ignore', invalid='ignore'):
        h = np.sinc(t) * np.cos(np.pi*alpha*t) / (1 - (2*alpha*t)**2)
    
    # Handle singularities at t = +/- 1/(2*alpha) where the denominator is 0
    if alpha != 0:
        h[np.isclose(np.abs(t), 1/(2*alpha))] = (np.pi/4) * np.sinc(1/(2*alpha))

    return h / np.sum(h)

def get_gauss_filter(BT, span, sps):
    t = np.arange(-span*sps//2, span*sps//2 + 1) / sps
    sigma = np.sqrt(np.log(2)) / (2 * np.pi * BT)
    h = np.exp(-t**2 / (2 * sigma**2))
    return h / np.sum(h)

def generate_pulse_train(pulse_type, bits, symbolRate, alpha, span, BT, sampling_frequency_hz):

    # Calculate bit duration
    bipolar_bits = np.where(bits == 1, 1, -1)
    samplesPerSymbol = int(sampling_frequency_hz/symbolRate)
    
    # Pre-calculate the expected length for time vector consistency
    expected_len = samplesPerSymbol * len(bits)
    pulse_train = np.zeros(expected_len)

    if pulse_type == 'Unipolar NRZ':
        pulse_train = np.repeat(bits, samplesPerSymbol)
    elif pulse_type == 'Polar NRZ':
        pulse_train = np.repeat(bipolar_bits, samplesPerSymbol)
    elif pulse_type == 'Unipolar RZ':
        for i, b in enumerate(bits):
            if b == 1:
                pulse_train[i*samplesPerSymbol : i*samplesPerSymbol + samplesPerSymbol//2] = 1
    elif pulse_type == 'Manchester':
        for i, b in enumerate(bits):
            if b == 1:
                pulse_train[i*samplesPerSymbol : i*samplesPerSymbol + samplesPerSymbol//2] = 1
                pulse_train[i*samplesPerSymbol + samplesPerSymbol//2 : (i+1)*samplesPerSymbol] = -1
            else:
                pulse_train[i*samplesPerSymbol : i*samplesPerSymbol + samplesPerSymbol//2] = -1
                pulse_train[i*samplesPerSymbol + samplesPerSymbol//2 : (i+1)*samplesPerSymbol] = 1
    
    # --- MODIFIED SECTION START ---
    elif pulse_type in ['Raised Cosine', 'Root Raised Cosine', 'Gaussian']:
        
        if pulse_type == 'Raised Cosine':
            h = get_rc_filter(alpha, span, samplesPerSymbol)
        elif pulse_type == 'Root Raised Cosine':
            h = get_rrc_filter(alpha, span, samplesPerSymbol)
        elif pulse_type == 'Gaussian':
            h = get_gauss_filter(BT, span, samplesPerSymbol)

        upsampled = np.zeros(expected_len)
        upsampled[::samplesPerSymbol] = bipolar_bits
        
        # Convolve
        raw_pulse = np.convolve(upsampled, h, mode='same')
        
        # Force length to match expected_len (Crop tails if single bit)
        if len(raw_pulse) > expected_len:
            diff = len(raw_pulse) - expected_len
            start = diff // 2
            pulse_train = raw_pulse[start : start + expected_len]
        else:
            pulse_train = raw_pulse
    # --- MODIFIED SECTION END ---

    else:
        raise ValueError("Unknown pulse type")

    # Normalize
    pulse_train = pulse_train / np.max(np.abs(pulse_train)) if np.max(np.abs(pulse_train)) != 0 else pulse_train

    # Time Vector
    time_vector = np.arange(len(pulse_train)) / sampling_frequency_hz

    return pulse_train, time_vector
