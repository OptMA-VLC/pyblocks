import numpy as np
from matplotlib import pyplot as plt

from src.pyblock import SignalWave
from src.pyblock_sim.entity.project.command.command_entity import CommandEntity, CommandType
from src.pyblock_sim.entity.project.command.plot_command_entity import PlotCommandEntity
from src.pyblock_sim.repository.signal_repository.signal_repository import SignalRepository


class RunCommandUseCase:
    _signal_repo: SignalRepository

    def __init__(self, signal_repo: SignalRepository):
        self._signal_repo = signal_repo

    def run_command(self, command: CommandEntity):
        if isinstance(command, PlotCommandEntity):
            self._run_plot_command(command)
        else:
            raise NotImplementedError(f"Unknown command type: '{command.type.value}'")

    def _run_plot_command(self, command: PlotCommandEntity):
        signals = {}
        for signal_selector in command.signals:
            try:
                signals[str(signal_selector)] = self._signal_repo.get(signal_selector.block, signal_selector.port)
            except KeyError:
                raise KeyError(f"The signal '{signal_selector}' can't be plotted because it was not found")

        fig, ax = plt.subplots()
        for (selector, signal) in signals.items():
            if isinstance(signal, np.ndarray):
                ax.plot(signal, label=str(selector))
            elif isinstance(signal, SignalWave):
                ax.plot(signal.time, signal.wave, label=str(selector))
            else:
                raise TypeError(
                    f"The signal {selector} can't be plotted because "
                    "plotting the type '{signal.type}' is not supported"
                )

        plt.legend()
        plt.show()
