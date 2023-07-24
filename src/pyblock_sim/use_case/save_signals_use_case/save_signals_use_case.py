from pathlib import Path
from typing import List

import numpy as np

from src.pyblock import TimeSignal
from src.pyblock_sim.entity.project.command.command_entity import CommandEntity, CommandType
from src.pyblock_sim.entity.project.signal_selector import SignalSelector
from src.pyblock_sim.repository.path_manager.path_manager import PathManager
from src.pyblock_sim.repository.signal_repository.signal_repository import SignalRepository
from src.pyblock_sim.use_case.save_signals_use_case.csv_saver import CSVSaver


class SaveSignalsUseCase:
    _signal_repo: SignalRepository
    _path_manager: PathManager

    def __init__(self, signal_repo: SignalRepository, path_manager: PathManager):
        self._signal_repo = signal_repo
        self._path_manager = path_manager

    def save_signals(self, command: CommandEntity):
        if command.type != CommandType.SAVE:
            raise ValueError(
                f"SaveCommandRunner.run(cmd) called with invalid command "
                f"type '{command.type}'. Must be '{CommandType.SAVE}'"
            )

        save_path = Path(command.get_param('save_path'))
        signals = self._parse_signals(command)

        resolved_save_path = self._path_manager.resolve_relpath_from_project(save_path)
        if not resolved_save_path.parent.exists():
            raise ValueError(
                f"The specified path to save the signals "
                f"'{resolved_save_path.resolve()}' does not exist"
            )

        # organize signals
        csv_signals_dict = {}
        str_signals_dict = {}
        for signal_selector in signals:
            signal = self._signal_repo.get_by_selector(signal_selector)
            if isinstance(signal, np.ndarray) or isinstance(signal, TimeSignal):
                csv_signals_dict[str(signal_selector)] = signal
            elif isinstance(signal, str):
                str_signals_dict[str(signal_selector)] = signal
            else:
                raise ValueError(f"Unsupported signal type for saving: {type(signal)}")

        # save strings
        with open(resolved_save_path, 'w') as f:
            for (name, signal) in str_signals_dict.items():
                if len(str_signals_dict) > 1:
                    f.write(f'>>>> {name}')
                f.write(signal)

        # save time series
        if len(csv_signals_dict) > 0:
            CSVSaver.save_csv(resolved_save_path, csv_signals_dict)

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
