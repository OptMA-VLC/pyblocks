from src.pyblock_sim.repository.cli.print_level import PrintLevel
from src.pyblock_sim.repository_provider import RepositoryProvider
from src.pyblock_sim.use_case.build_simulation_graph.build_simulation_graph_use_case import BuildSimulationGraphUseCase
from src.pyblock_sim.use_case.compute_simulation_steps.compute_simulation_steps_use_case import \
    ComputeSimulationStepsUseCase
from src.pyblock_sim.use_case.run_command.run_command_use_case import RunCommandUseCase
from src.pyblock_sim.use_case.simulate.simulate_use_case import SimulateUseCase


class RunFromFileUseCase:
    _repo_provider: RepositoryProvider

    def __init__(self, repo_provider: RepositoryProvider):
        self._repo_provider = repo_provider

    def run_from_file(self):
        cli = self._repo_provider.cli

        build_graph_use_case = BuildSimulationGraphUseCase(self._repo_provider.block_repo)
        compute_simulation_steps_use_case = ComputeSimulationStepsUseCase()
        simulate_use_case = SimulateUseCase(self._repo_provider.signal_repo, self._repo_provider.path_manager)
        run_command_use_case = RunCommandUseCase(self._repo_provider.signal_repo, self._repo_provider.path_manager)

        cli.print('Loading project............... ', end='')
        project = self._repo_provider.project_repo.load(
            self._repo_provider.path_manager.get_project_absolute_path()
        )
        cli.print('[green]ok[/green]', level=None)

        cli.print('Building simulation graph..... ', end='')
        simulation_graph = build_graph_use_case.build_simulation_graph(project.graph_spec)
        cli.print('[green]ok[/green]', level=None)

        cli.print('Computing simulation steps.... ', end='')
        simulation_steps = compute_simulation_steps_use_case.compute_simulation_steps(simulation_graph)
        cli.print('[green]ok[/green]', level=None)

        cli.print('Starting Simulation........... ', end='')
        simulation_report = simulate_use_case.simulate(simulation_steps)
        if simulation_report.success:
            cli.print('[green]ok[/green]', level=None)
        else:
            cli.print('[red]error[/red]', level=None)

        cli.print(simulation_report)

        for cmd in project.commands:
            cli.print(f'Running command {cmd.type.value}'.ljust(30, '.'), end=' ')
            try:
                run_command_use_case.run_command(cmd)
                cli.print('[green]ok[/green]', level=None)
            except Exception as ex:
                cli.print('[red]error[/red]', level=None)
                cli.print(f"Command {cmd.type.value} failed with the error - {ex}", level=PrintLevel.ERROR)
                break
