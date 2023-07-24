from src.pyblock_sim.repository.cli.print_level import PrintLevel
from src.pyblock_sim.repository_provider import RepositoryProvider
from src.pyblock_sim.use_case.run_command.run_command_use_case import RunCommandUseCase

from src.pyblock_sim.use_case.run_from_file.simulation_progress_printer import SimulationProgressPrinter
from src.pyblock_sim.use_case.simulate_use_case.simulate_use_case import SimulateUseCase


class RunFromFileUseCase:
    _repo_provider: RepositoryProvider

    def __init__(self, repo_provider: RepositoryProvider):
        self._repo_provider = repo_provider

    def run_from_file(self):
        cli = self._repo_provider.cli

        simulate_use_case = SimulateUseCase(
            self._repo_provider.signal_repo,
            self._repo_provider.block_repo,
            self._repo_provider.cli,
            self._repo_provider.path_manager
        )
        run_command_use_case = RunCommandUseCase(self._repo_provider.signal_repo, self._repo_provider.path_manager)

        cli.print('Loading project............... ', end='')
        project = self._repo_provider.project_repo.parse_project_file(
            self._repo_provider.path_manager.get_project_absolute_path()
        )
        cli.print('[green]ok[/green]', level=None)

        simulation_progress_printer = SimulationProgressPrinter(cli)
        simulate_use_case.simulate(project, simulation_progress_printer)

        for cmd in project.commands:
            cli.print(f'Running command {cmd.type.value}'.ljust(30, '.'), end=' ')
            try:
                run_command_use_case.run_command(cmd)
                cli.print('[green]ok[/green]', level=None)
            except Exception as ex:
                cli.print('[red]error[/red]', level=None)
                cli.print(f"Command {cmd.type.value} failed with the error - {ex}", level=PrintLevel.ERROR)
                break
