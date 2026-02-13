import numpy as np
import matplotlib.pyplot as plt
import plotly.express as px
from cycler import cycler
import os
import secrets

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
        if "trash" in fileName.lower():
            randomString = secrets.token_hex(16)
            fileName = fileName+randomString

        path = os.path.join("plots", f"{fileName.replace('.png','')}_{fig_idx}.png" if len(figures_data)>1 else f"{fileName.replace('.png','')}.png")
        if os.path.exists(path): raise FileExistsError(f"File {path} exists.")
        plt.savefig(path, dpi=1000)

    if show: plt.show()
    return created_figs

# =============================================================================
# 1. CORE FILTER MATHEMATICS
# =============================================================================

def get_raised_cosine_filter_unit_amplitude(time_vector, alpha, samples_per_symbol):
    if alpha == 0: alpha = 1e-8
    numerator = np.sinc(time_vector) * np.cos(np.pi * alpha * time_vector)
    denominator = 1 - (2 * alpha * time_vector)**2
    with np.errstate(divide='ignore', invalid='ignore'):
        h = numerator / denominator
    singularity_mask = np.isclose(denominator, 0, atol=1e-5)
    if np.any(singularity_mask):
        h[singularity_mask] = (np.pi / 4) * np.sinc(1 / (2 * alpha))
    return h

def get_root_raised_cosine_filter_unit_amplitude(time_vector, alpha, samples_per_symbol):
    if alpha == 0: alpha = 1e-8
    term1 = np.sin(np.pi * time_vector * (1 - alpha))
    term2 = (4 * alpha * time_vector) * np.cos(np.pi * time_vector * (1 + alpha))
    denominator = np.pi * time_vector * (1 - (4 * alpha * time_vector)**2)
    with np.errstate(divide='ignore', invalid='ignore'):
        h = (term1 + term2) / denominator
    h[np.isclose(time_vector, 0, atol=1e-7)] = 1.0 - alpha + (4 * alpha / np.pi)
    side_mask = np.isclose(np.abs(time_vector), 1 / (4 * alpha), atol=1e-5)
    if np.any(side_mask):
        val = (alpha / np.sqrt(2)) * ((1 + 2/np.pi) * np.sin(np.pi/4) + (1 - 2/np.pi) * np.cos(np.pi/4))
        h[side_mask] = val
    return h

def get_gaussian_filter_unit_amplitude(time_vector, BT, samples_per_symbol):
    # BT product determines the 3dB bandwidth
    c = -2 * np.pi**2 * (BT**2) / np.log(2)
    return np.exp(c * time_vector**2)

# =============================================================================
# 2. UNIFIED PULSE TRAIN GENERATOR
# =============================================================================

def generate_pulse_train(pulse_type, bits, symbol_rate, sampling_freq_hz, 
                         alpha=0.5, span=6, BT=0.3, 
                         delay_symbols=0.0, prefix_symbols=0, suffix_symbols=0,
                         truncate_tails=True, return_pulse_shape=False, 
                         debug_mode=False, external_t=None):
    
    if not isinstance(bits, np.ndarray):
        bits = np.array(bits)

    # --- Setup ---
    samples_per_symbol = int(sampling_freq_hz / symbol_rate)
    symbol_period_sec = 1 / symbol_rate
    num_symbols = len(bits)
    expected_length = num_symbols * samples_per_symbol
    total_symbols = prefix_symbols + num_symbols + suffix_symbols
    total_expected_length = total_symbols * samples_per_symbol

    debug_traces = []
    single_pulse_shape = None
    single_pulse_t = None

    # --- A. SHAPED PULSES (Summation of Delayed Pulses) ---
    if pulse_type in ['Raised Cosine', 'Root Raised Cosine', 'Gaussian']:
        bipolar_symbols = np.where(bits == 1, 1, -1)
        
        if external_t is not None:
            time_vector = external_t.copy()
        else:
            tail_duration_sec = (span / 2) * symbol_period_sec
            total_duration_sec = (total_symbols * symbol_period_sec) + (2 * tail_duration_sec)
            t_start = -tail_duration_sec
            time_vector = np.linspace(t_start, t_start + total_duration_sec, 
                                     int(total_duration_sec * sampling_freq_hz), endpoint=False)
        
        pulse_train = np.zeros_like(time_vector)

        for i, symbol_val in enumerate(bipolar_symbols):
            center_t = (prefix_symbols + delay_symbols + i + 0.5) * symbol_period_sec
            norm_t = (time_vector - center_t) / symbol_period_sec
            
            if pulse_type == 'Raised Cosine':
                pulse_shape = get_raised_cosine_filter_unit_amplitude(norm_t, alpha, samples_per_symbol)
            elif pulse_type == 'Root Raised Cosine':
                 pulse_shape = get_root_raised_cosine_filter_unit_amplitude(norm_t, alpha, samples_per_symbol)
            elif pulse_type == 'Gaussian':
                 pulse_shape = get_gaussian_filter_unit_amplitude(norm_t, BT, samples_per_symbol)
           
            mask = np.abs(norm_t) <= (span / 2)
            pulse_shape[~mask] = 0
            scaled_pulse = symbol_val * pulse_shape
            pulse_train += scaled_pulse
            
            if i == 0:
                single_pulse_shape = pulse_shape
                single_pulse_t = norm_t
            if debug_mode: debug_traces.append(scaled_pulse)

        if truncate_tails and external_t is None:
            start_idx = np.argmin(np.abs(time_vector))
            pulse_train = pulse_train[start_idx : start_idx + total_expected_length]
            time_vector = time_vector[start_idx : start_idx + total_expected_length]

    # --- B. RECTANGULAR PULSES (Masking Logic) ---
    elif pulse_type in ['Unipolar NRZ', 'Polar NRZ', 'Unipolar RZ', 'Manchester']:
        target_len = len(external_t) if external_t is not None else total_expected_length
        pulse_train = np.zeros(target_len)
        time_vector = external_t if external_t is not None else (np.arange(target_len) / sampling_freq_hz)

        def add_rect_pulse(idx, length_ratio, val, offset_ratio=0.0):
            t_start = (prefix_symbols + delay_symbols + idx + offset_ratio) * symbol_period_sec
            t_end = t_start + (symbol_period_sec * length_ratio)
            mask = (time_vector >= t_start) & (time_vector < t_end)
            pulse_train[mask] = val

        for k, bit in enumerate(bits):
            if pulse_type == 'Unipolar NRZ':
                if bit == 1: add_rect_pulse(k, 1.0, 1.0)
            elif pulse_type == 'Polar NRZ':
                add_rect_pulse(k, 1.0, 1.0 if bit == 1 else -1.0)
            elif pulse_type == 'Unipolar RZ':
                if bit == 1: add_rect_pulse(k, 0.5, 1.0)
            elif pulse_type == 'Manchester':
                v1, v2 = (1, -1) if bit == 1 else (-1, 1)
                add_rect_pulse(k, 0.5, v1, offset_ratio=0.0)
                add_rect_pulse(k, 0.5, v2, offset_ratio=0.5)

    # Final Normalization
    if np.max(np.abs(pulse_train)) != 0:
        pulse_train /= np.max(np.abs(pulse_train))

    return (pulse_train, time_vector, debug_traces) if debug_mode else (pulse_train, time_vector)

