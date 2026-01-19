import numpy as np
import matplotlib.pyplot as plt
import plotly.express as px
from cycler import cycler
import os

# --- 1. THEME DEFINITION (Fat Man) ---
AMMO_CRATE_GREEN = '#2e3b2b'
STENCIL_YELLOW = '#f0c808'
CHALK_WHITE = '#e0e0e0'
DANGER_RED = '#ff3333'
ENGRAVED_BLACK = '#1a2118'

# --- EXPANDED FATMAN PALETTE ---

# Standard Indicators
RAD_METER_ORANGE  = '#ff9900'  # High viz orange, good for secondary traces
WARNING_ORANGE    = '#e25822'  # Darker, "burnt" orange
CYAN_PRINT        = '#00e5ff'  # Blueprint/Oscilloscope cyan (high contrast)
HUD_TEAL          = '#40e0d0'  # Dull, vintage electronics teal

# Muted/Structural
STEEL_GRAY        = '#708090'  # Good for reference lines or noise floors
RUST_BROWN        = '#8b4513'  # For "decay" or interference traces
KHAKI_SAND        = '#c3b091'  # Neutral, organic trace

# Special Highlighting
PLASMA_BLUE       = '#6699cc'  # Soft glow blue
URANIUM_GREEN     = '#39ff14'  # "Radioactive" bright neon green (Use sparingly)


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
        'axes.prop_cycle': cycler(color=[CHALK_WHITE, DANGER_RED, STENCIL_YELLOW])
    })

# --- 2. THE ORGANIZER (UPDATED FOR WINDOWS + STACKS + OVERLAYS) ---
def auto_organize(xs, ys, layout, 
                  titles=None, legend_labels=None, 
                  xtitles=None, ytitles=None, 
                  colors=None, linestyles=None, 
                  legend_locs=None, jupiter_locs=None, # <--- NEW ARGUMENTS
                  **kwargs):
    """
    layout: A LIST OF LISTS.
            Outer List = Separate Figures (Windows).
            Inner List = Stacked Subplots within that Window.
            Integer    = Number of Traces overlaid on that Subplot.
            
            Example: [[3], [1, 1]]
            Figure 1: 1 Subplot with 3 traces overlaid.
            Figure 2: 2 Subplots stacked, 1 trace on each.
    """
    structure = []
    global_idx = 0
    
    # Iterate through WINDOWS (Outer List) using enumerate to get w_idx
    for w_idx, fig_layout in enumerate(layout):
        figure_payload = []
        
        # Iterate through SUBPLOTS (Inner List) using enumerate to get s_idx
        for s_idx, trace_count in enumerate(fig_layout):
            subplot_traces = []
            
            # --- 1. DETERMINE LOCATIONS FOR THIS SUBPLOT ---
            # We check if the lists exist and match the current indices
            curr_leg_loc = None
            if legend_locs and w_idx < len(legend_locs) and s_idx < len(legend_locs[w_idx]):
                curr_leg_loc = legend_locs[w_idx][s_idx]

            curr_jup_loc = None
            if jupiter_locs and w_idx < len(jupiter_locs) and s_idx < len(jupiter_locs[w_idx]):
                curr_jup_loc = jupiter_locs[w_idx][s_idx]

            # Iterate through TRACES (Integer Value)
            for _ in range(trace_count):
                if global_idx < len(xs):
                    d = {'x': xs[global_idx], 'y': ys[global_idx]}
                    
                    # Map metadata using the global index
                    if titles and global_idx < len(titles): d['title'] = titles[global_idx]
                    if xtitles and global_idx < len(xtitles): d['xlabel'] = xtitles[global_idx]
                    if ytitles and global_idx < len(ytitles): d['ylabel'] = ytitles[global_idx]
                    if legend_labels and global_idx < len(legend_labels): d['legend_label'] = legend_labels[global_idx]
                    if colors and global_idx < len(colors): d['color'] = colors[global_idx]
                    if linestyles and global_idx < len(linestyles): d['linestyle'] = linestyles[global_idx]
                    
                    # --- 2. INJECT LOCATIONS INTO TRACE DATA ---
                    if curr_leg_loc: d['legend_loc'] = curr_leg_loc
                    if curr_jup_loc: d['jupiter_loc'] = curr_jup_loc

                    # Apply defaults
                    for k, v in kwargs.items():
                        if k not in d: d[k] = v
                            
                    subplot_traces.append(d)
                    global_idx += 1
            figure_payload.append(subplot_traces)
        structure.append(figure_payload)
        
    return structure


import matplotlib.pyplot as plt
import os

# --- 3. THE PLOTTER (RENAMED TO MATPLOTLIB STYLE) ---
def plot_flex(figures_data, base_figsize=(10, 5), show=True, fileName="FatManPlot", 
              legend_loc='upper right', logo_loc='upper left'):
    """
    Renders multiple figures.
    
    Args:
        legend_loc: 'upper right', 'lower left', 'center', (0.5, 0.5), etc.
        logo_loc:   'upper left', 'lower right', 'center', (0.1, 0.9), etc.
    """
    apply_fatman_theme()
    created_figs = []
    
    if not os.path.exists("plots"):
        os.makedirs("plots")

    # --- LOCATION LOGIC (MATPLOTLIB STYLE) ---
    def get_logo_pos(loc_arg):
        # Map standard Matplotlib strings to explicit coordinates/alignment
        # Note: 'upper' vs 'top', 'lower' vs 'bottom'
        presets = {
            'upper left':   {'x': 0.02, 'y': 0.95, 'ha': 'left',  'va': 'top'},
            'upper right':  {'x': 0.98, 'y': 0.95, 'ha': 'right', 'va': 'top'},
            'lower left':   {'x': 0.02, 'y': 0.05, 'ha': 'left',  'va': 'bottom'},
            'lower right':  {'x': 0.98, 'y': 0.05, 'ha': 'right', 'va': 'bottom'},
            'center':       {'x': 0.50, 'y': 0.50, 'ha': 'center','va': 'center'},
            # Legacy support (optional, just in case)
            'top left':     {'x': 0.02, 'y': 0.95, 'ha': 'left',  'va': 'top'},
            'top right':    {'x': 0.98, 'y': 0.95, 'ha': 'right', 'va': 'top'},
            'bottom left':  {'x': 0.02, 'y': 0.05, 'ha': 'left',  'va': 'bottom'},
            'bottom right': {'x': 0.98, 'y': 0.05, 'ha': 'right', 'va': 'bottom'}
        }
        
        # Handle Tuple/Decimal Input
        if isinstance(loc_arg, (tuple, list)) and len(loc_arg) == 2:
            x, y = loc_arg
            ha = 'right' if x > 0.5 else 'left'
            va = 'top' if y > 0.5 else 'bottom'
            return {'x': x, 'y': y, 'ha': ha, 'va': va}
            
        # Default to upper left if key not found
        return presets.get(loc_arg, presets['upper left'])

    # Iterate through FIGURES
    for fig_idx, subplots_list in enumerate(figures_data):
        n = len(subplots_list) 
        
        fig, axes = plt.subplots(n, 1, figsize=(base_figsize[0], base_figsize[1] * n))
        if n == 1: axes = [axes] 
        
        # Iterate through SUBPLOTS
        for ax, trace_list in zip(axes, subplots_list):
            
            # --- 1. DETECT OVERRIDES ---
            first_trace = trace_list[0]
            
            # Use 'logo_loc' to match new naming convention
            # Fallback checks 'jupiter_loc' for backward compatibility with your organizer
            active_legend_loc = first_trace.get('legend_loc', legend_loc)
            active_logo_loc = first_trace.get('logo_loc', first_trace.get('jupiter_loc', logo_loc))

            # Draw Traces
            for data in trace_list:
                ax.plot(data['x'], data['y'], 
                        label=data.get('legend_label'),
                        color=data.get('color'),
                        linestyle=data.get('linestyle', '-')
                )
                if data.get('title'): ax.set_title(f">> {data['title']} <<", fontweight='bold', fontsize=13, pad=20)
                if data.get('xlabel'): ax.set_xlabel(data['xlabel'], fontweight='bold', fontsize=12)
                if data.get('ylabel'): ax.set_ylabel(data['ylabel'], fontweight='bold', fontsize=12, labelpad=10)

            # --- STYLING ---
            handles, labels = ax.get_legend_handles_labels()
            if labels:
                leg = ax.legend(frameon=True, loc=active_legend_loc)
                leg.get_frame().set_facecolor(ENGRAVED_BLACK)
                leg.get_frame().set_edgecolor(STENCIL_YELLOW)

            # --- JUPITER LOGO ---
            l_pos = get_logo_pos(active_logo_loc)
            ax.text(l_pos['x'], l_pos['y'], "JUPITER INDUSTRIES", transform=ax.transAxes, 
                    fontsize=9, color=AMMO_CRATE_GREEN, fontweight='bold',
                    verticalalignment=l_pos['va'],
                    horizontalalignment=l_pos['ha'],
                    bbox=dict(facecolor=STENCIL_YELLOW, edgecolor=STENCIL_YELLOW, boxstyle='square,pad=0.2'))

        fig.tight_layout()
        created_figs.append((fig, axes))
        
        # Save logic (omitted for brevity, same as before)
        if len(figures_data) > 1:
            clean_name = fileName.replace(".png", "")
            save_path = os.path.join("plots", f"{clean_name}_{fig_idx}.png")
        else:
            save_path = os.path.join("plots", fileName if fileName.endswith(".png") else f"{fileName}.png")
        if os.path.exists(save_path): raise FileExistsError(f"File '{save_path}' exists.")
        plt.savefig(save_path, dpi=600)

    if show: plt.show()
    return created_figs

def plot(xArg, yArg, xAxisTitle=0, yAxisTitle=0, plotTitle=0):
    fig = px.line(x=xArg, y=yArg)
    fig.update_layout(template="plotly_dark")
    fig.show()
    return 0

# --- 4. FILTER GENERATORS ---

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
    # Handle singularities at t = +/- 1/(2*alpha)
    if alpha != 0:
        h[np.isclose(np.abs(t), 1/(2*alpha))] = (np.pi/4) * np.sinc(1/(2*alpha))
    return h / np.sum(h)

def get_gauss_filter(BT, span, sps):
    t = np.arange(-span*sps//2, span*sps//2 + 1) / sps
    sigma = np.sqrt(np.log(2)) / (2 * np.pi * BT)
    h = np.exp(-t**2 / (2 * sigma**2))
    return h / np.sum(h)

# --- 5. PULSE GENERATORS (MODIFIED) ---

def genNRZPulse(pulseWidthArg,totalPulseWidthArg, samplingFrequencyHz = 100):
    pulseWidth = pulseWidthArg 
    totalPulseWidth = totalPulseWidthArg 
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
    # This is the old/simple generator
    samplesPerBit = int(bitDuration * samplingFrequencyHz)
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

def generate_pulse_train(pulse_type, bits, symbolRate, alpha, span, BT, sampling_frequency_hz, return_pulse_shape=False):
    """
    Generates a full pulse train based on input bits.
    If return_pulse_shape is True, also returns the single pulse shape (y) and its time vector (t).
    """

    # Calculate bit duration
    bipolar_bits = np.where(bits == 1, 1, -1)
    samplesPerSymbol = int(sampling_frequency_hz/symbolRate)
    
    # Pre-calculate the expected length for time vector consistency
    expected_len = samplesPerSymbol * len(bits)
    pulse_train = np.zeros(expected_len)

    # Placeholders for the single pulse data
    single_pulse_y = None
    single_pulse_t = None

    if pulse_type in ['Unipolar NRZ', 'Polar NRZ', 'Unipolar RZ', 'Manchester']:
        # For rectangular pulses, time is usually 0 to T_symbol
        single_pulse_t = np.arange(samplesPerSymbol) / sampling_frequency_hz
        single_pulse_y = np.zeros(samplesPerSymbol)

        if pulse_type == 'Unipolar NRZ':
            pulse_train = np.repeat(bits, samplesPerSymbol)
            single_pulse_y[:] = 1
        
        elif pulse_type == 'Polar NRZ':
            pulse_train = np.repeat(bipolar_bits, samplesPerSymbol)
            single_pulse_y[:] = 1 # Showing positive shape for visualization

        elif pulse_type == 'Unipolar RZ':
            single_pulse_y[:samplesPerSymbol//2] = 1
            for i, b in enumerate(bits):
                if b == 1:
                    pulse_train[i*samplesPerSymbol : i*samplesPerSymbol + samplesPerSymbol//2] = 1
        
        elif pulse_type == 'Manchester':
            single_pulse_y[:samplesPerSymbol//2] = 1
            single_pulse_y[samplesPerSymbol//2:] = -1
            for i, b in enumerate(bits):
                if b == 1:
                    pulse_train[i*samplesPerSymbol : i*samplesPerSymbol + samplesPerSymbol//2] = 1
                    pulse_train[i*samplesPerSymbol + samplesPerSymbol//2 : (i+1)*samplesPerSymbol] = -1
                else:
                    pulse_train[i*samplesPerSymbol : i*samplesPerSymbol + samplesPerSymbol//2] = -1
                    pulse_train[i*samplesPerSymbol + samplesPerSymbol//2 : (i+1)*samplesPerSymbol] = 1
    
    elif pulse_type in ['Raised Cosine', 'Root Raised Cosine', 'Gaussian']:
        
        # --- REGENERATE TIME VECTOR FOR SINGLE PULSE ---
        single_pulse_t = np.arange(-span*samplesPerSymbol//2, span*samplesPerSymbol//2 + 1) / samplesPerSymbol

        if pulse_type == 'Raised Cosine':
            h = get_rc_filter(alpha, span, samplesPerSymbol)
        elif pulse_type == 'Root Raised Cosine':
            h = get_rrc_filter(alpha, span, samplesPerSymbol)
        elif pulse_type == 'Gaussian':
            h = get_gauss_filter(BT, span, samplesPerSymbol)
        
        single_pulse_y = h # Store kernel for return

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

    else:
        raise ValueError("Unknown pulse type")

    # Normalize
    pulse_train = pulse_train / np.max(np.abs(pulse_train)) if np.max(np.abs(pulse_train)) != 0 else pulse_train

    # Time Vector
    time_vector = np.arange(len(pulse_train)) / sampling_frequency_hz

    if return_pulse_shape:
        return pulse_train, time_vector, single_pulse_y, single_pulse_t
    
    return pulse_train, time_vector