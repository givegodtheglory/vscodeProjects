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

#Archived pulse functions. Deprecated since when I tried to form pulse trains, they
#do not accept time vector arguments and so I end up with trailing and prefix zeros
#creating discontinuites in the pulseTrain. 
""" 
def get_rrc_filter(alpha, span, sps):
    t = np.arange(-span*sps//2, span*sps//2 + 1) / sps
    if alpha == 0: alpha = 1e-8
    h = np.zeros(len(t))
    idx_0 = np.isclose(t, 0, atol=1e-8)
    h[idx_0] = 1 - alpha + (4 * alpha / np.pi)
    denom_check = 1 - (4 * alpha * t)**2
    idx_sing = np.isclose(denom_check, 0, atol=1e-5) & (~idx_0)
    if np.any(idx_sing):
        val = (alpha / np.sqrt(2)) * ((1 + 2/np.pi) * np.sin(np.pi/(4*alpha)) + (1 - 2/np.pi) * np.cos(np.pi/(4*alpha)))
        h[idx_sing] = val
    idx_rest = ~(idx_0 | idx_sing)
    t_r = t[idx_rest]
    num = (np.sin(np.pi * t_r * (1 - alpha)) + 4 * alpha * t_r * np.cos(np.pi * t_r * (1 + alpha)))
    denom = (np.pi * t_r * (1 - (4 * alpha * t_r)**2))
    h[idx_rest] = num / denom
    return h / np.sqrt(np.sum(h**2))

def get_rc_filter(alpha, span, sps):
    t = np.arange(-span*sps//2, span*sps//2 + 1) / sps
    if alpha == 0: alpha = 1e-8
    num = np.sinc(t) * np.cos(np.pi * alpha * t)
    denom = 1 - (2 * alpha * t)**2
    with np.errstate(divide='ignore', invalid='ignore'):
        h = num / denom
    singularity_mask = np.isclose(denom, 0, atol=1e-5)
    h[singularity_mask] = (np.pi / 4) * np.sinc(1 / (2 * alpha))
    return h / np.sum(h) * sps 

def get_gauss_filter(BT, span, sps):
    t = np.arange(-span*sps//2, span*sps//2 + 1) / sps
    sigma = np.sqrt(np.log(2)) / (2 * np.pi * BT)
    h = (1 / (np.sqrt(2 * np.pi) * sigma)) * np.exp(-(t**2) / (2 * sigma**2))
    return h / np.sum(h) * sps
 """


def pulsetr(fun, alpha, numberOfPointsPerSymbolInterval, filterSpan, data):
    """
    Generates a pulse train y, given a transmission pulse sequence in data
    and a function 'fun' that generates the basic pulse.
    
    Parameters:
    - fun:   The function object (or name) to generate the pulse (e.g., rc_pulse).
             Must accept inputs (alpha, time_vector).
    - alpha:     Pulse parameter (e.g., alpha/roll-off).
    - numberOfPointsPerSymbolInterval:     Number of points per symbol interval (oversampling factor).
    - Pulse width: Total width of the pulse in symbol intervals.
    - data:  The sequence of symbols (amplitudes).
    
    Returns:
    - y:     The generated pulse train.
    - t:     The time vector used for the single pulse.
    """
    
    # --- 1. Setup Time Vector for the Basic Pulse ---
    # MATLAB: int = 1/n; t = -width/2:int:width/2;
    # Python: We use linspace for better floating point precision than arange
    samples_per_pulse = int(filterSpan * numberOfPointsPerSymbolInterval + 1)
    symbolTimeVector = np.linspace(-filterSpan/2, filterSpan/2, samples_per_pulse)
    
    lt = len(symbolTimeVector)
    len_data = len(data)
    
    # --- 2. Calculate Output Size ---
    # MATLAB: num = n * (width + len - 1) + 1;
    # (Total samples needed to accommodate the overlapping pulses)
    total_samples = int(numberOfPointsPerSymbolInterval * (filterSpan + len_data - 1) + 1)
    
    # --- 3. Generate Basic Pulse ---
    # MATLAB: x = feval(fun, a, t);
    # Python: We call the function object directly
    x = fun(alpha, symbolTimeVector)
    
    # --- 4. Superpose Pulses ---
    y = np.zeros(total_samples)
    
    for k in range(len_data):
        # Calculate the starting index (offset)
        # MATLAB: tmp = n*(k-1)  (1-based indexing)
        # Python: offset = n*k   (0-based indexing)
        offset = k * numberOfPointsPerSymbolInterval
        
        # Add the weighted pulse to the correct slice of y
        # This replaces the inefficient [zeros... x ... zeros] concatenation
        y[offset : offset + lt] += x * data[k]
        
    return y, symbolTimeVector

def get_raised_cosine_filter_unit_amplitude(time_vector, rolloff_factor, samples_per_symbol):
    """
    Computes the Raised Cosine (RC) filter impulse response for a given time vector.

    The Raised Cosine filter is widely used in digital communications to shape pulses
    to minimize Inter-Symbol Interference (ISI). It satisfies the Nyquist ISI criterion,
    meaning the pulse is 1 at t=0 and 0 at all other symbol intervals (t = +/-1, +/-2...).

    Mathematical Formula:
                 sin(pi * t/T)       cos(pi * alpha * t/T)
        h(t) =  ---------------  * -----------------------
                   pi * t/T          1 - (2 * alpha * t/T)^2

        Where:
        - T is the symbol period (normalized to 1.0 in this function).
        - alpha is the rolloff factor (0 to 1).
        - The first term is a standard Sinc function (ideal low-pass filter).
        - The second term tapers the Sinc tails to reduce ISI sensitivity to timing jitter.

    Args:
        time_vector (np.array): 
            Array of time indices normalized by the symbol period.
            - t = 0.0 corresponds to the center of the pulse (peak).
            - t = 1.0 corresponds to the time of the next symbol.
            - Example: np.linspace(-3, 3, 61) covers 3 symbols before and after.

        rolloff_factor (float): 
            The excess bandwidth parameter (alpha), 0 <= alpha <= 1.
            - alpha = 0: Converges to a pure Sinc function (brick-wall filter).
            - alpha = 1: Decays faster but uses twice the bandwidth.
            - Controls the trade-off between bandwidth efficiency and timing sensitivity.

        samples_per_symbol (int): 
            The number of samples representing one symbol period.
            Used to normalize the filter energy so the gain is unity.

    Returns:
        np.array: The normalized impulse response evaluated at the points in `time_vector`.
    """
    
    # --- Pre-computation Safety Check ---
    # If alpha is exactly 0, the denominator logic 1-(2at)^2 simplifies to 1.
    # We nudge it slightly to 1e-8 to avoid strict zero-division issues in the
    # singularity check without materially changing the result.
    if rolloff_factor == 0:
        rolloff_factor = 1e-8

    # --- Step 1: Calculate the Numerator ---
    # The numerator is the product of a Sinc function and a Cosine term.
    # Formula: sinc(t) * cos(pi * alpha * t)
    sinc_part = np.sinc(time_vector)
    cos_part = np.cos(np.pi * rolloff_factor * time_vector)
    numerator = sinc_part * cos_part

    # --- Step 2: Calculate the Denominator ---
    # The denominator introduces a potential singularity when 1 - (2 * alpha * t)^2 = 0.
    # This happens when t = +/- 1 / (2 * alpha).
    denominator = 1 - (2 * rolloff_factor * time_vector)**2

    # --- Step 3: Perform Division with Safety Handling ---
    # We expect division by zero at the singularity points calculated above.
    # We suppress warnings here and manually fix the invalid values in Step 4.
    with np.errstate(divide='ignore', invalid='ignore'):
        h = numerator / denominator

    # --- Step 4: Handle Singularities (L'Hôpital's Rule) ---
    # At t = +/- 1 / (2 * alpha), the limit of the function is:
    # Limit = (pi / 4) * sinc(1 / (2 * alpha))
    singularity_mask = np.isclose(denominator, 0, atol=1e-5)
    
    if np.any(singularity_mask):
        limit_val = (np.pi / 4) * np.sinc(1 / (2 * rolloff_factor))
        h[singularity_mask] = limit_val

    # --- Step 5: Normalize Peak Amplitude ---
    # Normalize so that the sum of coefficients equals samples_per_symbol.
    # This ensures that a constant stream of 1s produces a unity gain output.
    if np.sum(h) != 0:
        h = h / np.max(np.abs(h)) 

    return h

def get_root_raised_cosine_filter(time_vector, rolloff_factor, samples_per_symbol):
    """
    Computes the Root Raised Cosine (RRC) filter impulse response for a given time vector.

    The RRC filter is the "square root" of the RC filter in the frequency domain.
    It is typically used in a matched filter pair: one RRC filter at the Transmitter (TX)
    and one identical RRC filter at the Receiver (RX). 
    
    Note: A single RRC pulse does NOT satisfy the Nyquist ISI criterion. 
    Zero ISI is only achieved after the signal has passed through *both* filters:
    H_total(f) = H_RRC(f) * H_RRC(f) = H_RC(f).

    Mathematical Formula:
               sin(pi*t*(1-a)) + 4*a*t * cos(pi*t*(1+a))
        h(t) = -----------------------------------------
                   pi * t * (1 - (4*a*t)^2)

        Where:
        - t is the normalized time (t/T).
        - a is the rolloff factor (alpha).
        - The numerator is a SUM of a sine term and a scaled cosine term.
        - The denominator has a singularity at t = +/- 1/(4a).

    Args:
        time_vector (np.array): 
            Array of time indices normalized by the symbol period.
            - t = 0.0 corresponds to the center of the pulse.
        
        rolloff_factor (float): 
            The excess bandwidth parameter (alpha), 0 <= alpha <= 1.
        
        samples_per_symbol (int): 
            The number of samples representing one symbol period.

    Returns:
        np.array: The normalized impulse response evaluated at the points in `time_vector`.
    """

    # --- Pre-computation Safety Check ---
    if rolloff_factor == 0:
        rolloff_factor = 1e-8

    # --- Step 1: Calculate Numerator Terms ---
    # Unlike the RC filter (product), the RRC numerator is a SUM of two terms.
    
    # Term A: sin(pi * t * (1-alpha))
    term1 = np.sin(np.pi * time_vector * (1 - rolloff_factor))
    
    # Term B: 4 * alpha * t * cos(pi * t * (1+alpha))
    # This term is scaled linearly by time 't'.
    term2 = (4 * rolloff_factor * time_vector) * np.cos(np.pi * time_vector * (1 + rolloff_factor))
    
    numerator = term1 + term2

    # --- Step 2: Calculate Denominator ---
    # The denominator singularity occurs when 1 - (4 * alpha * t)^2 = 0.
    # This implies t = +/- 1 / (4 * alpha).
    # There is also a singularity at t=0 due to the (pi * t) term.
    denominator = np.pi * time_vector * (1 - (4 * rolloff_factor * time_vector)**2)

    # --- Step 3: Perform Division with Safety Handling ---
    with np.errstate(divide='ignore', invalid='ignore'):
        h = numerator / denominator

    # --- Step 4: Handle Singularities ---
    
    # Case A: The Peak at t = 0
    # The limit as t -> 0 is: 1 - alpha + (4 * alpha / pi)
    peak_mask = np.isclose(time_vector, 0, atol=1e-5)
    if np.any(peak_mask):
        h[peak_mask] = 1 - rolloff_factor + (4 * rolloff_factor / np.pi)
        
    # Case B: The Side Singularities at t = +/- 1 / (4 * alpha)
    # The denominator becomes zero here. Using L'Hôpital's rule, we calculate the limit.
    side_mask = np.isclose(np.abs(time_vector), 1 / (4 * rolloff_factor), atol=1e-5)
    if np.any(side_mask):
        # Specific limit value for this RRC form
        val = (rolloff_factor / np.sqrt(2)) * (
            (1 + 2/np.pi) * np.sin(np.pi/4) + (1 - 2/np.pi) * np.cos(np.pi/4)
        )
        h[side_mask] = val

    # --- Step 5: Normalize Energy ---
    # Standard normalization for discrete time simulation.
    if np.sum(h) != 0:
        h = h / np.sum(h) * samples_per_symbol

    return h

def get_gaussian_filter(time_vector, bt_product, samples_per_symbol):
    """
    Computes the Gaussian filter impulse response for a given time vector.

    The Gaussian filter is used in modulation schemes like GMSK (GSM) and FSK.
    Unlike RC/RRC, it does NOT satisfy the Nyquist zero-ISI criterion (it causes ISI).
    However, it has optimal time-frequency localization, meaning it provides the
    smoothest possible transitions between bits. This eliminates zero-crossing 
    jitter and reduces spectral regrowth in non-linear power amplifiers.

    Mathematical Formula:
        h(t) = B * sqrt(2*pi / ln(2)) * exp( -2 * pi^2 * B^2 * t^2 / ln(2) )

        Where:
        - B is the Bandwidth-Time product (BT).
        - ln(2) relates to the half-power (3dB) bandwidth.
        - The pulse is a pure exponential bell curve.

    Args:
        time_vector (np.array): 
            Array of time indices normalized by the symbol period.
        
        bt_product (float): 
            The Bandwidth-Time product (e.g., 0.3 or 0.5).
            - Small BT (e.g., 0.3): Narrow Bandwidth -> Wider Pulse in Time -> More ISI.
            - Large BT (e.g., 1.0): Wide Bandwidth -> Sharper Pulse in Time -> Less ISI.
        
        samples_per_symbol (int): 
            The number of samples representing one symbol period.

    Returns:
        np.array: The normalized impulse response evaluated at the points in `time_vector`.
    """
    
    # --- Step 1: Define Gaussian Constants ---
    # These constants are derived from the requirement that 'B' represents the 3dB bandwidth.
    ln2 = np.log(2)
    
    # Amplitude Coefficient: B * sqrt(2*pi / ln2)
    amplitude_factor = (np.sqrt(2 * np.pi / ln2) * bt_product)
    
    # Exponent Coefficient: -2 * pi^2 * B^2 / ln2
    # Note: BT is in the numerator. A smaller BT makes the exponent smaller,
    # resulting in a slower decay (wider pulse).
    exponent_factor = - (2 * np.pi**2 * bt_product**2 / ln2)
    
    # --- Step 2: Compute the Exponential ---
    # h(t) = A * exp( C * t^2 )
    # This calculation is safe for all t; there are no singularities in a Gaussian.
    h = amplitude_factor * np.exp(exponent_factor * time_vector**2)
    
    # --- Step 3: Normalize Energy ---
    # The Gaussian pulse theoretically extends to infinity. 
    # We normalize by the sum of the samples in our finite window to ensure Unity Gain.
    if np.sum(h) != 0:
        h = h / np.sum(h) * samples_per_symbol
        
    return h

def generate_pulse_train(pulse_type, bits, symbol_rate, alpha, span, BT, sampling_freq_hz, truncate_tails=True, return_pulse_shape=False, debug_mode=False):
    """
    Generates a pulse train. 
    
    Args:
        truncate_tails (bool): If True, cuts the start/end filter tails so the output length 
                               is EXACTLY (num_symbols * samples_per_symbol). 
                               Fixes 'operands could not be broadcast' errors.
    """
    
    # --- 1. COMMON SETUP ---
    bipolar_symbols = np.where(bits == 1, 1, -1)
    samples_per_symbol = int(sampling_freq_hz / symbol_rate)
    symbol_period_sec = 1 / symbol_rate
    num_symbols = len(bits)
    
    # Calculate the exact expected length (without tails)
    expected_length = num_symbols * samples_per_symbol
    
    debug_traces = []
    single_pulse_shape = None
    single_pulse_t = None
    pulse_train = None
    time_vector = None

    # =========================================================================
    # BRANCH A: SHAPED PULSES (RC, RRC, Gaussian)
    # Uses Shift & Add, then truncates tails if requested
    # =========================================================================
    if pulse_type in ['Raised Cosine', 'Root Raised Cosine', 'Gaussian']:
        
        # A1. Define Global Time Vector (WITH TAILS initially)
        # We need the tails for the math to work, even if we cut them later.
        tail_duration_sec = (span / 2) * symbol_period_sec
        total_duration_sec = (num_symbols * symbol_period_sec) + (2 * tail_duration_sec)
        
        t_start = -tail_duration_sec
        t_end = t_start + total_duration_sec
        total_samples = int(total_duration_sec * sampling_freq_hz)
        
        time_vector = np.linspace(t_start, t_end, total_samples, endpoint=False)
        pulse_train = np.zeros_like(time_vector)

        # A2. Loop and Sum
        for i, symbol_val in enumerate(bipolar_symbols):
            
            # Shift time relative to current symbol center
            current_symbol_center_time = i * symbol_period_sec
            shifted_time_sec = time_vector - current_symbol_center_time
            normalized_shifted_time = shifted_time_sec / symbol_period_sec
            
            # Compute Pulse
            if pulse_type == 'Raised Cosine':
                pulse_shape = get_raised_cosine_filter_unit_amplitude(normalized_shifted_time, alpha, samples_per_symbol)
            
            elif pulse_type == 'Root Raised Cosine':

                 pulse_shape = get_root_raised_cosine_filter(normalized_shifted_time, alpha, samples_per_symbol)
            
            elif pulse_type == 'Gaussian':
                 pulse_shape = get_gaussian_filter(normalized_shifted_time, alpha, samples_per_symbol)
           
            # Enforce Span
            mask = np.abs(normalized_shifted_time) <= (span / 2)
            pulse_shape[~mask] = 0
            
            # Superposition
            scaled_pulse = symbol_val * pulse_shape
            pulse_train += scaled_pulse
            
            # Debug Capture
            if i == 0:
                single_pulse_shape = pulse_shape
                single_pulse_t = normalized_shifted_time
            
            if debug_mode:
                debug_traces.append(scaled_pulse)

        # A3. Truncate Tails (Crucial Fix)
        if truncate_tails:
            # We determine where the "Data" actually starts (t=0)
            # Find the index closest to t=0
            start_idx = np.argmin(np.abs(time_vector))
            
            # Slice exactly 'expected_length' samples from that point
            # This drops the negative-time tail and the post-sequence tail
            if start_idx + expected_length <= len(pulse_train):
                pulse_train = pulse_train[start_idx : start_idx + expected_length]
                time_vector = time_vector[start_idx : start_idx + expected_length]
            else:
                # Fallback if rounding errors make array slightly too short
                pulse_train = pulse_train[start_idx:]
                time_vector = time_vector[start_idx:]
            
            if debug_mode and len(debug_traces) > 0:
                 # Truncate traces too
                 debug_traces = [d[start_idx : start_idx + expected_length] for d in debug_traces]

    # =========================================================================
    # BRANCH B: RECTANGULAR PULSES (NRZ, RZ, Manchester)
    # Uses Simple Construction (No tails, always matches expected_length)
    # =========================================================================
    elif pulse_type in ['Unipolar NRZ', 'Polar NRZ', 'Unipolar RZ', 'Manchester']:
        
        # B1. Create the Raw Pulse Stream
        raw_pulse = np.zeros(expected_length)
        
        if pulse_type == 'Unipolar NRZ':
            raw_pulse = np.repeat(bits, samples_per_symbol)
            
        elif pulse_type == 'Polar NRZ':
            raw_pulse = np.repeat(bipolar_symbols, samples_per_symbol)
            
        elif pulse_type == 'Unipolar RZ':
            half_sps = samples_per_symbol // 2
            one_template = np.zeros(samples_per_symbol)
            one_template[:half_sps] = 1 # High for first half
            
            for k, bit in enumerate(bits):
                if bit == 1:
                    start = k * samples_per_symbol
                    raw_pulse[start : start+samples_per_symbol] = one_template

        elif pulse_type == 'Manchester':
            half_sps = samples_per_symbol // 2
            for k, bit in enumerate(bits):
                start = k * samples_per_symbol
                mid = start + half_sps
                end = start + samples_per_symbol
                
                if bit == 1: # 1 -> High-Low
                    raw_pulse[start:mid] = 1
                    raw_pulse[mid:end] = -1
                else:        # 0 -> Low-High
                    raw_pulse[start:mid] = -1
                    raw_pulse[mid:end] = 1

        pulse_train = raw_pulse
        time_vector = np.arange(len(pulse_train)) / sampling_freq_hz
        
        # Dummy return shapes
        single_pulse_shape = np.ones(samples_per_symbol)
        single_pulse_t = np.linspace(0, 1, samples_per_symbol)

    else:
        raise ValueError(f"Unknown pulse type: {pulse_type}")

    # --- 3. FINAL NORMALIZATION ---
    if np.max(np.abs(pulse_train)) != 0:
        max_val = np.max(np.abs(pulse_train))
        pulse_train = pulse_train / max_val
        if debug_mode and len(debug_traces) > 0:
            debug_traces = [d / max_val if np.max(np.abs(d))!=0 else d for d in debug_traces]

    # --- 4. RETURNS ---
    if debug_mode:
        return pulse_train, time_vector, debug_traces

    if return_pulse_shape:
        if single_pulse_shape is not None and pulse_type in ['Raised Cosine', 'Root Raised Cosine', 'Gaussian']:
             valid_indices = np.where(np.abs(single_pulse_t) <= span/2)[0]
             return pulse_train, time_vector, single_pulse_shape[valid_indices], single_pulse_t[valid_indices]
        return pulse_train, time_vector, None, None
    
    return pulse_train, time_vector