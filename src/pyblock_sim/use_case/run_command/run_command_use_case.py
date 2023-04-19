import csv
from pathlib import Path

import numpy as np
from matplotlib import pyplot as plt

from src.pyblock import TimeSignal
from src.pyblock_sim.entity.project.command.command_entity import CommandEntity
from src.pyblock_sim.entity.project.command.plot_command_entity import PlotCommandEntity
from src.pyblock_sim.entity.project.command.save_command_entity import SaveCommandEntity
from src.pyblock_sim.repository.signal_repository.signal_repository import SignalRepository


class RunCommandUseCase:
    _signal_repo: SignalRepository

    def __init__(self, signal_repo: SignalRepository):
        self._signal_repo = signal_repo

    def run_command(self, command: CommandEntity):
        if isinstance(command, PlotCommandEntity):
            self._run_plot_command(command)
        elif isinstance(command, SaveCommandEntity):
            self._run_save_command(command)
        else:
            raise NotImplementedError(f"Unknown command type: '{command.type.value}'")

    def _run_plot_command(self, command: PlotCommandEntity):
        signals = {}
        for signal_selector in command.signals:
            try:
                signals[str(signal_selector)] = self._signal_repo.get_by_selector(signal_selector)
            except KeyError:
                raise KeyError(f"The signal '{signal_selector}' can't be plotted because it was not found")

        fig, ax = plt.subplots(1, 1, figsize=(10, 6))
        for (selector, signal) in signals.items():
            if isinstance(signal, np.ndarray):
                ax.plot(signal, label=str(selector))
            elif isinstance(signal, TimeSignal):
                ax.plot(signal.time, signal.wave, label=str(selector))
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

        if command.save_path is not None:
            save_path = Path(command.save_path)
            if not save_path.parent.exists():
                raise ValueError(f"The specified path to save the plot '{save_path.resolve()}' does not exist")
            plt.savefig(save_path)

        plt.show()

    def _run_save_command(self, command: SaveCommandEntity):
        save_path = Path(command.save_path)
        if not save_path.parent.exists():
            raise ValueError(f"The specified path to save the signals '{save_path.resolve()}' does not exist")

        signals_table = []
        for signal_selector in command.signals:
            try:
                signal = self._signal_repo.get_by_selector(signal_selector)
                if isinstance(signal, np.ndarray):
                    sig_list = signal.tolist()
                    arr = [str(signal_selector)] + sig_list
                    signals_table.append(arr)
                elif isinstance(signal, TimeSignal):
                    arr_time = [f'{signal_selector} (time)'] + signal.time.tolist()
                    arr_wave = [f'{signal_selector} (signal)'] + signal.wave.tolist()
                    signals_table.append(arr_time)
                    signals_table.append(arr_wave)
                else:
                    raise TypeError(f"Saving signal of type '{type(signal)}' is not supported")
            except KeyError:
                raise KeyError(f"The signal '{signal_selector}' can't be saved because it was not found")

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
