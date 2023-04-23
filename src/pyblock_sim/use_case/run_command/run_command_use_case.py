import csv
from pathlib import Path

import numpy as np
from matplotlib import pyplot as plt

from src.pyblock import TimeSignal
from src.pyblock_sim.entity.project.command.command_entity import CommandEntity
from src.pyblock_sim.entity.project.command.plot_command_entity import PlotCommandEntity
from src.pyblock_sim.entity.project.command.save_command_entity import SaveCommandEntity
from src.pyblock_sim.repository.signal_repository.signal_repository import SignalRepository
from src.pyblock_sim.use_case.run_command.csv_saver import CSVSaver
from src.pyblock_sim.use_case.run_command.plotter import Plotter


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

        Plotter.line_plot(signals, Path(command.save_path))

    def _run_save_command(self, command: SaveCommandEntity):
        save_path = Path(command.save_path)
        if not save_path.parent.exists():
            raise ValueError(f"The specified path to save the signals '{save_path.resolve()}' does not exist")

        csv_signals_dict = {}
        str_signals_dict = {}
        for signal_selector in command.signals:
            signal = self._signal_repo.get_by_selector(signal_selector)
            if isinstance(signal, np.ndarray) or isinstance(signal, TimeSignal):
                csv_signals_dict[str(signal_selector)] = signal
            elif isinstance(signal, str):
                str_signals_dict[str(signal_selector)] = signal
            else:
                raise ValueError(f"Unsupported signal type for saving: {type(signal)}")

        if len(str_signals_dict) > 0:
            with open(save_path, 'w') as f:
                for (name, signal) in str_signals_dict.items():
                    if len(str_signals_dict) > 1:
                        f.write(f'>>>> {name}')
                    f.write(signal)

        if len(csv_signals_dict) > 0:
            CSVSaver.save_csv(Path(save_path), csv_signals_dict)



