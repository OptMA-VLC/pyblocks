from abc import ABC, abstractmethod
from typing import Any

from src.pyblock_sim.use_case.param_sweep_use_case.param_sweep_result import IterationResult, ParamSweepResult


class SweepProgressCallbacks(ABC):
    @abstractmethod
    def will_start_sweep(self):
        pass

    @abstractmethod
    def will_start_iteration(self, iteration_number: int, total_iterations: int, iteration_value: Any):
        pass

    @abstractmethod
    def did_finish_iteration(self, iteration_result: IterationResult):
        pass

    @abstractmethod
    def did_finish_sweep(self, result: ParamSweepResult):
        pass
