from pathlib import Path
from typing import Optional, Dict, Any

import numpy as np
from matplotlib import pyplot as plt

from src.pyblock import TimeSignal


class Plotter:
    @staticmethod
    def line_plot(signals: Dict[str, Any], save_path: Optional[Path] = None):
        fig, ax = plt.subplots(1, 1, figsize=(10, 6))

        for (selector, signal) in signals.items():
            if isinstance(signal, np.ndarray):
                ax.plot(signal, label=str(selector))
            elif isinstance(signal, TimeSignal):
                ax.plot(signal.time, signal.signal, label=str(selector))
            else:
                raise TypeError(
                    f"The signal {selector} can't be plotted because "
                    f"plotting the type '{type(signal).__name__}' is not supported"
                )

        # Shrink current axis by 20%
        box = ax.get_position()
        ax.set_position([box.x0, box.y0, box.width * 0.8, box.height])

        # Put a legend to the right of the current axis
        ax.legend(loc='center left', bbox_to_anchor=(1, 0.5))

        if save_path is not None:
            if not save_path.parent.exists():
                raise ValueError(f"The specified path to save the plot '{save_path.resolve()}' does not exist")
            plt.savefig(save_path)

        plt.show()

