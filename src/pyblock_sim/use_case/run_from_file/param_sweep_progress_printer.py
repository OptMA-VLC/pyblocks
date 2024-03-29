from typing import Any

from src.pyblock_sim.entity.parameter_sweep.param_sweep_result_entity import ParamSweepResultEntity, \
    IterationResultEntity
from src.pyblock_sim.repository.cli.cli import CLI
from src.pyblock_sim.use_case.param_sweep_use_case.sweep_progress_callbacks import SweepProgressCallbacks


class ParamSweepProgressPrinter(SweepProgressCallbacks):
    _cli: CLI

    def __init__(self, cli: CLI):
        self._cli = cli

    def will_start_sweep(self):
        self._cli.print("============================================================")
        self._cli.print("Starting Parameter Sweep\n")
        self._cli.print()

    def will_start_iteration(self, iteration_number: int, total_iterations: int, iteration_value: Any):
        self._cli.print(f"Iteration {iteration_number} with param value = {iteration_value}")

    def did_finish_iteration(self, iteration_result: IterationResultEntity):
        pass

    def did_finish_sweep(self, result: ParamSweepResultEntity):
        if result.success:
            self._cli.print('[green]Parameter sweep completed successfully[/green]')
        else:
            self._cli.print('[red]Parameter sweep failed.[/red]')

        self._cli.print('============================================================')
