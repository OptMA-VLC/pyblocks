import csv
from pathlib import Path
from typing import Dict

import numpy as np

from src.pyblock import TimeSignal


class CSVSaver:
    @staticmethod
    def save_csv(save_path: Path, signals: Dict):
        if len(signals) == 0:
            return

        signals_table = []
        for (sig_name, signal) in signals.items():
            if isinstance(signal, np.ndarray):
                arr = [sig_name] + signal.tolist()
                signals_table.append(arr)
            elif isinstance(signal, TimeSignal):
                arr_time = [f'{sig_name} (time)'] + signal.time.tolist()
                arr_wave = [f'{sig_name} (signal)'] + signal.wave.tolist()
                signals_table.append(arr_time)
                signals_table.append(arr_wave)
            else:
                raise TypeError(f"Saving signal of type '{type(signal)}' as csv is not supported")

        with open(save_path, 'w', newline='') as f:
            writer = csv.writer(f)
            headers = []
            max_len = 0
            for signal_list in signals_table:
                headers.append(signal_list[0])
                if len(signal_list) > max_len:
                    max_len = len(signal_list)

            writer.writerow(headers)
            for i in range(1, max_len):
                row = []
                for signal_list in signals_table:
                    try:
                        row.append(signal_list[i])
                    except IndexError:
                        row.append(None)
                writer.writerow(row)
