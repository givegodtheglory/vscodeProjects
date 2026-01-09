import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import welch
from ipywidgets import interact, FloatSlider, IntSlider
from helperFunctions import generate_pulse_train

# --- Static parameters ---
numberOfSymbols = 1000
symbolRate = 10
samplingFreqHz = 10001
span = 10

def simulate_fsk(alpha, BT, carrierFrequencyHz, fskFreqOffsetHz):
    bits = np.random.randint(0, 2, numberOfSymbols)

    dataPulseTrain, t = generate_pulse_train(
        'Polar NRZ', bits, symbolRate, alpha, span, BT, samplingFreqHz
    )

    modulatedFrequency = carrierFrequencyHz + (dataPulseTrain * fskFreqOffsetHz)
    angleArgument = 2 * np.pi * modulatedFrequency * t
    fskSignal = np.cos(angleArgument)

    freqs, psd = welch(fskSignal, samplingFreqHz, nperseg=4096)

    # --- Plot ---
    plt.figure(figsize=(10, 6))


    plt.plot(freqs, 10*np.log10(psd))
    plt.title("PSD (Welch)")

    plt.tight_layout()
    plt.show()


# --- Interactive sliders ---
interact(
    simulate_fsk,
    alpha=FloatSlider(min=0.0, max=1.0, step=0.05, value=0.35, description="Rolloff α"),
    BT=FloatSlider(min=0.1, max=1.0, step=0.05, value=0.3, description="BT"),
    carrierFrequencyHz=IntSlider(min=500, max=5000, step=100, value=2000, description="Carrier"),
    fskFreqOffsetHz=IntSlider(min=50, max=1000, step=50, value=200, description="FSK Δf"),
)