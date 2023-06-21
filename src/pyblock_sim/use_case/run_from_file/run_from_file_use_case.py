from pathlib import Path

from src.pyblock_sim.repository_provider import RepositoryProvider
from src.pyblock_sim.use_case.build_simulation_graph.build_simulation_graph_use_case import BuildSimulationGraphUseCase
from src.pyblock_sim.use_case.compute_simulation_steps.compute_simulation_steps_use_case import \
    ComputeSimulationStepsUseCase
from src.pyblock_sim.use_case.run_command.run_command_use_case import RunCommandUseCase
from src.pyblock_sim.use_case.simulate.simulate_use_case import SimulateUseCase
from src.pyblock_sim.use_case.simulate.simulation_report import SimulationReport
from src.pyblock_sim.util.logger import logger


class RunFromFileUseCase:
    _repo_provider: RepositoryProvider

    def __init__(self, repo_provider: RepositoryProvider):
        self._repo_provider = repo_provider

    def run_from_file(self, project_path: Path):
        build_graph_use_case = BuildSimulationGraphUseCase(self._repo_provider.block_repo)
        compute_simulation_steps_use_case = ComputeSimulationStepsUseCase()
        simulate_use_case = SimulateUseCase(
            self._repo_provider.signal_repo,
            self._repo_provider.block_repo
        )
        run_command_use_case = RunCommandUseCase(self._repo_provider.signal_repo)

        logger.info('Loading project............... ', end='')
        project = self._repo_provider.project_repo.load(project_path)
        logger.info('[green]ok[/green]', no_tag=True)

        logger.info('Building simulation graph..... ', end='')
        simulation_graph = build_graph_use_case.build_simulation_graph(project.graph_spec)
        logger.info('[green]ok[/green]', no_tag=True)

        logger.info('Computing simulation steps.... ', end='')
        simulation_steps = compute_simulation_steps_use_case.compute_simulation_steps(simulation_graph)
        logger.info('[green]ok[/green]', no_tag=True)

        logger.info('Starting Simulation........... ', end='')
        simulation_report = simulate_use_case.simulate(simulation_steps)
        if simulation_report.success:
            logger.info('[green]ok[/green]', no_tag=True)
        else:
            logger.info('[red]error[/red]', no_tag=True)

        self._print_simulation_report(simulation_report)

        for cmd in project.commands:
            logger.info(f'Running command {cmd.type.value}'.ljust(30, '.'), end=' ')
            try:
                run_command_use_case.run_command(cmd)
                logger.info('[green]ok[/green]', no_tag=True)
            except Exception as ex:
                logger.info('[red]error[/red]', no_tag=True)
                logger.error(f"Command {cmd.type.value} failed with the error - {ex}")
                break

    def _print_simulation_report(self, report: SimulationReport):
        logger.info('========================= Simulation Report =========================')
        num_steps = len(report.steps)
        i = 0
        for step in report.steps:
            i += 1
            block_name = f'Block {str(step.block_instance_id).ljust(25)}'
            exec_time = f'time: {step.execution_time:.2f} s'
            logger.info(f"Step {i}/{num_steps} - {block_name} - {exec_time} - ", end='')
            if step.success:
                logger.info('[green]ok[/green]', no_tag=True)
            else:
                logger.info('[red]error[/red]', no_tag=True)
                logger.info(f'Step failed with error: {step.exception}')
                logger.info(f'The following error caused this failure: {step.exception.inner_exception}')
        logger.info('=====================================================================\n')

