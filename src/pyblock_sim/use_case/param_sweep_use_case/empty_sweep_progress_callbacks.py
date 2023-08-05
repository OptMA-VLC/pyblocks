from typing import Any

from src.pyblock_sim.use_case.param_sweep_use_case.param_sweep_result import IterationResult, ParamSweepResult
from src.pyblock_sim.use_case.param_sweep_use_case.sweep_progress_callbacks import SweepProgressCallbacks


class EmptySweepProgressCallbacks(SweepProgressCallbacks):
    def will_start_sweep(self):
        pass

    def will_start_iteration(self, iteration_number: int, total_iterations: int, iteration_value: Any):
        pass

    def did_finish_iteration(self, iteration_result: IterationResult):
        pass

    def did_finish_sweep(self, result: ParamSweepResult):
        pass
