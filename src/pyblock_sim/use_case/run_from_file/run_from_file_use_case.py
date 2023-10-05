from src.pyblock_sim.entity.project.command.command_entity import CommandType, CommandEntity
from src.pyblock_sim.entity.project.project_entity import ProjectEntity
from src.pyblock_sim.repository.cli.print_level import PrintLevel
from src.pyblock_sim.repository.param_sweep_result_repository.param_sweep_result_repository import \
    ParamSweepResultRepository
from src.pyblock_sim.repository.repository_provider import RepositoryProvider
from src.pyblock_sim.use_case.block_help_use_case.block_help_use_case import BlockHelpUseCase
from src.pyblock_sim.use_case.param_sweep_use_case.param_sweep_use_case import ParamSweepUseCase
from src.pyblock_sim.use_case.plot_signals_use_case.plot_signals_use_case import PlotSignalsUseCase
from src.pyblock_sim.use_case.run_from_file.param_sweep_progress_printer import ParamSweepProgressPrinter

from src.pyblock_sim.use_case.run_from_file.simulation_progress_printer import SimulationProgressPrinter
from src.pyblock_sim.use_case.save_signals_use_case.save_signals_use_case import SaveSignalsUseCase
from src.pyblock_sim.use_case.simulate_use_case.simulate_use_case import SimulateUseCase


class RunFromFileUseCase:
    _repo_provider: RepositoryProvider

    def __init__(self, repo_provider: RepositoryProvider):
        self._repo_provider = repo_provider

    def run_from_file(self):
        cli = self._repo_provider.cli

        self._load_blocks()
        project = self._load_project()

        if len(project.commands) == 0:
            cli.print('There are no commands in this project file. The simulator will exit.')
            return

        for command in project.commands:
            try:
                cli.print(f'Running command [bold]{command.type.value}[/bold]')
                if command.type == CommandType.SIMULATE:
                    self._simulate_use_case(project)
                elif command.type == CommandType.PARAMETER_SWEEP:
                    self._simulate_sweep_use_case(command, project)
                elif command.type == CommandType.PLOT:
                    self._plot_signals_use_case(command)
                elif command.type == CommandType.SAVE:
                    self._save_signals_use_case(command)
                elif command.type == CommandType.BLOCK_HELP:
                    self._block_help_use_case(command)
                else:
                    raise NotImplementedError(f"Unknown command type: '{command.type.value}'")
            except Exception as e:
                cli.print(f'Command [bold]{command.type.value}[/bold] failed with exception:', level=PrintLevel.ERROR)
                cli.print(f'{e}', level=PrintLevel.ERROR)
                cli.print('The simulator will now exit by rethrowing this exception...')
                raise

    def _load_blocks(self):
        cli = self._repo_provider.cli

        cli.print('Loading block library......... ', end='')
        library_path = self._repo_provider.path_manager.get_block_library_absolute_path()
        indexing_result = self._repo_provider.block_repo.index_blocks(library_path)
        cli.print('[green]ok[/green]', level=None)
        cli.print(indexing_result)

    def _load_project(self):
        cli = self._repo_provider.cli

        cli.print('Loading project............... ', end='')
        project = self._repo_provider.project_repo.parse_project_file(
            self._repo_provider.path_manager.get_project_absolute_path()
        )
        cli.print('[green]ok[/green]', level=None)

        return project

    def _simulate_use_case(self, project: ProjectEntity):
        simulate_use_case = SimulateUseCase(
            self._repo_provider.signal_repo,
            self._repo_provider.block_repo,
            self._repo_provider.path_manager
        )
        simulation_progress_printer = SimulationProgressPrinter(self._repo_provider.cli)
        simulation_report = simulate_use_case.simulate(project, simulation_progress_printer)
        if not simulation_report.success:
            raise simulation_report.exception


    def _simulate_sweep_use_case(self, command: CommandEntity, project: ProjectEntity):
        simulate_sweep_use_case = ParamSweepUseCase(
            self._repo_provider.signal_repo,
            self._repo_provider.block_repo,
            self._repo_provider.path_manager
        )
        sweep_progress_printer = ParamSweepProgressPrinter(self._repo_provider.cli)

        sweep_result = simulate_sweep_use_case.simulate_sweep(
            command, project, sweep_progress_printer
        )

        save_path_str = command.get_param('output_dir')
        save_path = self._repo_provider.path_manager.resolve_relpath_from_project(save_path_str)
        self._repo_provider.cli.print(f'Now saving parameter sweep result to {save_path}')

        save_sweep_repo = ParamSweepResultRepository()
        save_sweep_repo.save_result(sweep_result, save_path)

        self._repo_provider.cli.print('Saved parameter sweep data.')

    def _plot_signals_use_case(self, command: CommandEntity):
        plot_signals_use_case = PlotSignalsUseCase(
            self._repo_provider.signal_repo, self._repo_provider.path_manager
        )
        plot_signals_use_case.plot_signals(command)

    def _save_signals_use_case(self, command: CommandEntity):
        save_signals_use_case = SaveSignalsUseCase(
            self._repo_provider.signal_repo, self._repo_provider.path_manager
        )
        save_signals_use_case.save_signals(command)

    def _block_help_use_case(self, command: CommandEntity):
        block_help_use_case = BlockHelpUseCase(
            self._repo_provider.block_repo, self._repo_provider.cli
        )
        block_help_use_case.print_block_help(command)
