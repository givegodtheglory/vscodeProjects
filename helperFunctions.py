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

# --- 1. THE ORGANIZER ---
def auto_organize(xs, ys, layout, 
                  titles=None, legend_labels=None, 
                  xtitles=None, ytitles=None, 
                  colors=None, linestyles=None, 
                  legend_locs=None, logo_locs=None,
                  xlims=None, ylims=None,
                  plot_types=None,
                  **kwargs):
    
    structure = []
    global_idx = 0
    
    # Helper: Universal Prop Extractor
    def get_nested_prop(source_list, w_idx, s_idx, t_idx, g_idx):
        if not source_list: return None
        try:
            val = source_list[w_idx][s_idx]
            if isinstance(val, list): return val[t_idx] 
            elif isinstance(val, str) and t_idx == 0: return val 
        except (IndexError, TypeError): pass

        try:
            val = source_list[w_idx][s_idx]
            if isinstance(val, str): return val
        except (IndexError, TypeError): pass

        if g_idx < len(source_list): return source_list[g_idx]
        return None

    for w_idx, fig_layout in enumerate(layout):
        figure_payload = []
        for s_idx, trace_count in enumerate(fig_layout):
            subplot_traces = []
            
            curr_leg = legend_locs[w_idx][s_idx] if (legend_locs and w_idx < len(legend_locs) and s_idx < len(legend_locs[w_idx])) else None
            curr_logo = logo_locs[w_idx][s_idx] if (logo_locs and w_idx < len(logo_locs) and s_idx < len(logo_locs[w_idx])) else None
            curr_xlim = xlims[w_idx][s_idx] if (xlims and w_idx < len(xlims) and s_idx < len(xlims[w_idx])) else None
            curr_ylim = ylims[w_idx][s_idx] if (ylims and w_idx < len(ylims) and s_idx < len(ylims[w_idx])) else None

            for t_idx in range(trace_count):
                if global_idx < len(xs):
                    d = {'x': xs[global_idx], 'y': ys[global_idx]}
                    
                    if titles and global_idx < len(titles): d['title'] = titles[global_idx]
                    if xtitles and global_idx < len(xtitles): d['xlabel'] = xtitles[global_idx]
                    if ytitles and global_idx < len(ytitles): d['ylabel'] = ytitles[global_idx]
                    if legend_labels and global_idx < len(legend_labels): d['legend_label'] = legend_labels[global_idx]
                    if colors and global_idx < len(colors): d['color'] = colors[global_idx]
                    if linestyles and global_idx < len(linestyles): d['linestyle'] = linestyles[global_idx]
                    
                    found_type = get_nested_prop(plot_types, w_idx, s_idx, t_idx, global_idx)
                    d['type'] = found_type if found_type else 'line'
                    
                    if curr_leg: d['legend_loc'] = curr_leg
                    if curr_logo: d['logo_loc'] = curr_logo
                    if curr_xlim: d['xlim'] = curr_xlim
                    if curr_ylim: d['ylim'] = curr_ylim
                    
                    for k, v in kwargs.items():
                        if k not in d: d[k] = v

                    subplot_traces.append(d)
                    global_idx += 1
            figure_payload.append(subplot_traces)
        structure.append(figure_payload)
    return structure


# --- 2. THE PLOTTER ---
def plot_flex(figures_data, base_figsize=(10, 5), show=True, fileName="FatManPlot", 
              legend_loc='upper right', logo_loc='upper left'):
    
    if 'apply_fatman_theme' in globals(): globals()['apply_fatman_theme']()
    if not os.path.exists("plots"): os.makedirs("plots")
    
    created_figs = []

    def get_logo_pos(loc_arg):
        presets = {'upper left': {'x':0.02,'y':0.95,'ha':'left','va':'top'},
                   'upper right':{'x':0.98,'y':0.95,'ha':'right','va':'top'},
                   'lower left': {'x':0.02,'y':0.05,'ha':'left','va':'bottom'},
                   'lower right':{'x':0.98,'y':0.05,'ha':'right','va':'bottom'}}
        if isinstance(loc_arg, (tuple, list)) and len(loc_arg) == 2:
            return {'x':loc_arg[0], 'y':loc_arg[1], 'ha':'left', 'va':'top'}
        return presets.get(loc_arg, presets['upper left'])

    for fig_idx, subplots_list in enumerate(figures_data):
        n = len(subplots_list)
        fig, axes = plt.subplots(n, 1, figsize=(base_figsize[0], base_figsize[1] * n))
        if n == 1: axes = [axes]

        for ax, trace_list in zip(axes, subplots_list):
            first = trace_list[0]
            if first.get('xlim'): ax.set_xlim(first['xlim'])
            if first.get('ylim'): ax.set_ylim(first['ylim'])
            act_leg = first.get('legend_loc', legend_loc)
            act_logo = first.get('logo_loc', logo_loc)

            for data in trace_list:
                raw = data.get('type', 'line')
                if isinstance(raw, list): raw = raw[0]
                p_type = str(raw).lower().strip()
                
                col = data.get('color')
                lbl = data.get('legend_label')
                
                print(f"[DEBUG] Drawing '{p_type}' for label: {lbl}")

                if p_type == 'scatter':
                    ax.scatter(data['x'], data['y'], label=lbl, color=col, s=20, alpha=0.9)
                
                elif p_type == 'stem':
                    use_col = col if col else STENCIL_YELLOW 
                    marker, stemlines, baseline = ax.stem(data['x'], data['y'], 
                                                          linefmt=use_col, markerfmt='o',
                                                          label=lbl, basefmt=" ")
                    plt.setp(stemlines, color=use_col, linewidth=1.5)
                    plt.setp(marker, color=use_col, markerfacecolor=use_col, markeredgecolor=use_col, markersize=6)
                    plt.setp(baseline, visible=False)

                # --- [NEW] DIGITAL PLOT (Stem + Step) ---
                elif p_type == 'digital':
                    use_col = col if col else STENCIL_YELLOW
                    
                    # 1. Draw the Step (The Horizontal Connection)
                    # where='post' means the line goes horizontal, then vertical (classic digital look)
                    ax.step(data['x'], data['y'], color=use_col, where='post', linewidth=1.5, label=lbl)
                    
                    # 2. Draw the Stems (The Vertical Drops)
                    marker, stemlines, baseline = ax.stem(data['x'], data['y'], 
                                                          linefmt=use_col, markerfmt='o',
                                                          basefmt=" ") # No label here to avoid double legend
                    
                    plt.setp(stemlines, color=use_col, linewidth=1.5)
                    plt.setp(marker, color=use_col, markerfacecolor=use_col, markeredgecolor=use_col, markersize=6)
                    plt.setp(baseline, visible=False)

                elif p_type == 'step':
                    ax.step(data['x'], data['y'], label=lbl, color=col, where='post', linewidth=1.5)

                else:
                    ax.plot(data['x'], data['y'], label=lbl, color=col, linestyle=data.get('linestyle', '-'))

                if data.get('title'): ax.set_title(data['title'], fontweight='bold', fontsize=13)
                if data.get('xlabel'): ax.set_xlabel(data['xlabel'], fontweight='bold')
                if data.get('ylabel'): ax.set_ylabel(data['ylabel'], fontweight='bold')

            if ax.get_legend_handles_labels()[1]:
                leg = ax.legend(frameon=True, loc=act_leg)
                leg.get_frame().set_facecolor(ENGRAVED_BLACK)
                leg.get_frame().set_edgecolor(STENCIL_YELLOW)

            lp = get_logo_pos(act_logo)
            ax.text(lp['x'], lp['y'], "JUPITER INDUSTRIES", transform=ax.transAxes,
                    fontsize=9, color=AMMO_CRATE_GREEN, fontweight='bold', va=lp['va'], ha=lp['ha'],
                    bbox=dict(facecolor=STENCIL_YELLOW, edgecolor=STENCIL_YELLOW, boxstyle='square,pad=0.2'))

        fig.tight_layout()
        created_figs.append((fig, axes))
        
        path = os.path.join("plots", f"{fileName.replace('.png','')}_{fig_idx}.png" if len(figures_data)>1 else f"{fileName.replace('.png','')}.png")
        if os.path.exists(path): raise FileExistsError(f"File {path} exists.")
        plt.savefig(path, dpi=1000)

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