from typing import Type

from src.pyblock_sim.entity.simulation.simulation_report import SimulationReport
from src.pyblock_sim.repository.cli.object_printer import ObjectPrinter


class SimulationReportPrinter(ObjectPrinter):
    def get_type(self) -> Type:
        return SimulationReport

    def print(self, report: SimulationReport) -> str:
        s = '========================= Simulation Report =========================\n'

        num_steps = len(report.steps)
        i = 0
        for step in report.steps:
            i += 1
            block_name = f'Block {str(step.block_instance_id).ljust(25)}'
            exec_time = f'time: {step.execution_time:.2f} s'
            s += f"Step {i}/{num_steps} - {block_name} - {exec_time} - "

            if step.success:
                s += '[green]ok[/green]\n'
            else:
                s += '[red]error[/red]\n'
                s += f'  [red]>>[/red] Step failed with error: {step.exception}\n'
                s += f'  [red]>>[/red] This error was caused by the exception: {step.exception.inner_exception}\n'

        s += '=====================================================================\n'
        return s
