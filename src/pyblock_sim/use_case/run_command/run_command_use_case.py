from pathlib import Path

import numpy as np

from src.pyblock import TimeSignal
from src.pyblock_sim.entity.project.command.command_entity import CommandEntity, CommandType
from src.pyblock_sim.entity.project.command.plot_command_entity import PlotCommandEntity
from src.pyblock_sim.entity.project.command.save_command_entity import SaveCommandEntity
from src.pyblock_sim.repository.path_manager.path_manager import PathManager
from src.pyblock_sim.repository.signal_repository.signal_repository import SignalRepository
from src.pyblock_sim.use_case.run_command.csv_saver import CSVSaver
from src.pyblock_sim.use_case.run_command.plot_command_runner import PlotCommandRunner
from src.pyblock_sim.use_case.run_command.plotter import Plotter
from src.pyblock_sim.use_case.run_command.save_command_runner import SaveCommandRunner


class RunCommandUseCase:
    _signal_repo: SignalRepository
    _path_manager: PathManager

    def __init__(self, signal_repo: SignalRepository, path_manager: PathManager):
        self._signal_repo = signal_repo
        self._path_manager = path_manager

    def run_command(self, command: CommandEntity):
        if command.type == CommandType.PLOT:
            runner = PlotCommandRunner(self._signal_repo, self._path_manager)
            runner.run(command)
        elif command.type == CommandType.SAVE:
            runner = SaveCommandRunner(self._signal_repo, self._path_manager)
            runner.run(command)
        else:
            raise NotImplementedError(f"Unknown command type: '{command.type.value}'")
