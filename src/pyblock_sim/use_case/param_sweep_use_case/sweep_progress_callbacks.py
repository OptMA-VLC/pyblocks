from abc import ABC, abstractmethod
from typing import Any

from src.pyblock_sim.entity.parameter_sweep.param_sweep_result_entity import IterationResultEntity, \
    ParamSweepResultEntity


class SweepProgressCallbacks(ABC):
    @abstractmethod
    def will_start_sweep(self):
        pass

    @abstractmethod
    def will_start_iteration(self, iteration_number: int, total_iterations: int, iteration_value: Any):
        pass

    @abstractmethod
    def did_finish_iteration(self, iteration_result: IterationResultEntity):
        pass

    @abstractmethod
    def did_finish_sweep(self, result: ParamSweepResultEntity):
        pass
