from typing import Any

from src.pyblock_sim.repository.cli.cli import CLI
from src.pyblock_sim.use_case.param_sweep_use_case.param_sweep_result import ParamSweepResult, IterationResult
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
        iter_cnt = f'{iteration_number}/{total_iterations}'
        self._cli.print(f"Iteration {iter_cnt} with param value = {iteration_value}")

    def did_finish_iteration(self, iteration_result: IterationResult):
        pass

    def did_finish_sweep(self, result: ParamSweepResult):
        if result.success:
            self._cli.print('[green]Parameter sweep completed successfully[/green]')
        else:
            self._cli.print('[red]Parameter sweep failed.[/red]')

        self._cli.print('============================================================')
