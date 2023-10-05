from typing import List

from src.pyblock_sim.entity.graph.simulation_graph import SimulationGraph
from src.pyblock_sim.entity.simulation.simulation_report import SimulationReport
from src.pyblock_sim.entity.simulation.simulation_step_report import SimulationStepReport
from src.pyblock_sim.entity.simulation.simulation_steps import SimulationStep
from src.pyblock_sim.repository.cli.cli import CLI
from src.pyblock_sim.use_case.simulate_use_case.simulation_progress_callbacks import SimulationProgressCallbacks


class SimulationProgressPrinter(SimulationProgressCallbacks):
    _cli: CLI

    def __init__(self, cli: CLI):
        self._cli = cli

    def will_start_simulation(self):
        self._cli.print('======== Beginning Simulation ========')

    def will_build_simulation_graph(self):
        self._cli.print('Building simulation graph..... ', end='')

    def did_build_simulation_graph(self, simulation_graph: SimulationGraph):
        self._cli.print('[green]ok[/green]', level=None)

    def will_calculate_steps(self):
        self._cli.print('Computing simulation steps.... ', end='')

    def did_calculate_steps(self, simulation_steps: List[SimulationStep]):
        self._cli.print('[green]ok[/green]', level=None)
        self._cli.print(f'The simulation consists of {len(simulation_steps)} steps.')
        self._cli.print('Starting Step Executions...... ')

    def will_simulate_step(self):
        pass

    def did_simulate_step(self, step_report: SimulationStepReport):
        block_name = f'Block {str(step_report.block_instance_id).ljust(25)}'
        exec_time = f'time: {step_report.execution_time:.2f} s'
        step_count = f'{step_report.step_number + 1}/{step_report.total_number_of_steps}'
        s = f"  Step {step_count} - {block_name} - {exec_time} - "

        if step_report.success:
            s += '[green]ok[/green]'
        else:
            s += '[red]error[/red]\n'
            s += f'    [red]>>[/red] Step failed with error: {step_report.exception}\n'
            s += f'    [red]>>[/red] This error was caused by the exception: {step_report.exception.inner_exception}'

        self._cli.print(s)

    def did_complete_simulation(self, simulation_report: SimulationReport):
        self._cli.print('========== Simulation Ended ==========')
