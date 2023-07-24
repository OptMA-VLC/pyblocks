from pathlib import Path
from typing import List, Optional

from src.pyblock_sim.entity.project.signal_selector import SignalSelector
from src.pyblock_sim.repository.path_manager.path_manager import PathManager
from src.pyblock_sim.repository.signal_repository.signal_repository import SignalRepository
from src.pyblock_sim.use_case.plot_signals_use_case.plotter import Plotter


class PlotSignalsUseCase:
    _signal_repo: SignalRepository
    _path_manager: PathManager

    def __init__(self, signal_repo: SignalRepository, path_manager: PathManager):
        self._signal_repo = signal_repo
        self._path_manager = path_manager

    def plot_signals(self, signals: List[SignalSelector], save_path: Optional[Path] = None):
        signals_dict = {}

        for signal_selector in signals:
            try:
                signals_dict[str(signal_selector)] = self._signal_repo.get_by_selector(signal_selector)
            except KeyError:
                raise KeyError(f"The signal '{signal_selector}' can't be plotted because it was not found")

        if save_path is not None:
            save_path = self._path_manager.resolve_relpath_from_project(Path(save_path))

        Plotter.line_plot(signals_dict, save_path)

    def _parse_signals(self, command: CommandEntity) -> List[SignalSelector]:
        signals_raw = command.get_param('signals')
        if not isinstance(signals_raw, List):
            raise ValueError(
                f"The 'signals' parameter of the {command.type} command "
                f"must be of type 'List' but got type '{type(signals_raw)}'"
            )

        parsed_signals = []
        for signal in signals_raw:
            parsed_signals.append(SignalSelector.parse(signal))

        return parsed_signals
