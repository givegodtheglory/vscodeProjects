import matplotlib.pyplot as plt
from matplotlib import font_manager
import os

# ---------------------------------------------------------
# CONFIGURATION
# ---------------------------------------------------------

# List the font names you want to preview.
# These must match the internal font family names on your system.
# You can add as many as you want.
FONTS = [
    "Drafting Mono",
    "Drafting Script",
    "ISOCP",
    "ISOCT",
    "Futura",
    "Eurostile",
    "Microgramma",
    "Bank Gothic",
    "IBM Plex Mono",
    "VT323",
    "Source Sans Pro",
    "Source Code Pro",
]

# Sample text to display
SAMPLE = "The quick brown fox — DSP/Comms Test"

# Font size for preview
FONT_SIZE = 20

# ---------------------------------------------------------
# OPTIONAL: Add custom .ttf files manually
# ---------------------------------------------------------
# Example:
# font_manager.fontManager.addfont("/path/to/your/font.ttf")
# After adding, use the font's internal name in FONTS list.


# ---------------------------------------------------------
# PLOT GENERATION
# ---------------------------------------------------------

def preview_fonts(font_list, sample_text=SAMPLE, fontsize=FONT_SIZE):
    n = len(font_list)
    fig, axes = plt.subplots(n, 1, figsize=(12, n * 1.2))

    if n == 1:
        axes = [axes]

    for ax, font_name in zip(axes, font_list):
        try:
            ax.text(
                0.01, 0.5, sample_text,
                fontname=font_name,
                fontsize=fontsize,
                va="center",
                ha="left"
            )
            ax.set_title(font_name, fontsize=fontsize)
        except Exception as e:
            ax.text(0.01, 0.5, f"Font not found: {font_name}", fontsize=fontsize)
            ax.set_title(font_name, fontsize=fontsize)

        ax.set_xticks([])
        ax.set_yticks([])
        ax.set_frame_on(False)

    plt.tight_layout()
    plt.show()


# ---------------------------------------------------------
# RUN
# ---------------------------------------------------------

preview_fonts(FONTS)