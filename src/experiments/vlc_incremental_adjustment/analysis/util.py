import json
from typing import Dict

import numpy as np


def pretty_print_dict(my_dict: Dict) -> str:
    return json.dumps(my_dict, indent=4, sort_keys=True)


def plot_as_text(time: np.array, signal: np.array, width=80, height=8):
    # Create an empty grid for the waveform plot
    waveform_grid = [[' ' for _ in range(width)] for _ in range(height)]

    # Determine the scaling factors for time and signal
    time_min, time_max = np.min(time), np.max(time)
    signal_min, signal_max = np.min(signal), np.max(signal)

    time_scale = width / (time_max - time_min)
    signal_scale = height / (signal_max - signal_min)

    # Map time and signal values to coordinates within the grid
    for t, s in zip(time, signal):
        x = int((t - time_min) * time_scale)
        y = int((s - signal_min) * signal_scale)

        # Ensure the coordinates are within the grid bounds
        if 0 <= y < height and 0 <= x < width:
            waveform_grid[y][x] = '.'

    # Convert the grid to a string
    waveform_str = '\n'.join([''.join(row) for row in waveform_grid])

    return waveform_str
