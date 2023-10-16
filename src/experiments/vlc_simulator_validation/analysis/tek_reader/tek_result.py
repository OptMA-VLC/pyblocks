from typing import Dict

import numpy as np

from src.experiments.vlc_simulator_validation.analysis.util.util import pretty_print_dict, plot_as_text


class TekResult:
    time: np.array
    signal: np.array
    metadata: Dict

    def __str__(self):
        s = '---- TekCsv object ----\n\nMetadata:'
        s += pretty_print_dict(self.metadata)
        s += '\n\nWaveForm:\n'
        s += plot_as_text(self.time, self.signal)
        return s

    def __sub__(self, other: 'TekResult') -> 'TekResult':
        res = TekResult()
        res.time = self.time
        res.signal = self.signal - other.signal
        return res
