from typing import List

import numpy as np
from matplotlib import pyplot as plt, cm

from src.experiments.vlc_simulator_validation.analysis.tek_reader.tek_result import TekResult


def sample_signals(
    signals: List[TekResult], sample_times: List[float]
) -> List[List[float]]:
    color_iter = iter(cm.rainbow(np.linspace(0.9, 1, len(signals))))
    for signal in signals:
        color = next(color_iter)
        plt.plot(signal.time, signal.signal, linewidth=0.5, c=color)
    ymin, ymax = plt.gca().get_ylim()
    plt.vlines(sample_times, ymin, ymax, color='k', linestyles='dashed')
    plt.grid()
    plt.show()

    samples = []
    for time in sample_times:
        samples_for_time_n = []
        for signal in signals:
            samples_for_time_n.append(signal.value_at_time(time))
        samples.append(samples_for_time_n)

    return samples
