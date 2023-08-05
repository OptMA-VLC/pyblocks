from dataclasses import dataclass
from typing import Any, List

from src.pyblock_sim.repository.signal_repository.signal_repository import SignalRepository
from src.pyblock_sim.use_case.simulate_use_case.simulation_report import SimulationReport


@dataclass
class IterationResult:
    iteration_number: int
    iteration_value: Any
    report: SimulationReport
    signal_repo: SignalRepository

    @property
    def success(self) -> bool:
        return self.report.success


class ParamSweepResult:
    target_block: str
    target_param: str
    param_values: List[Any]
    iteration_results: List[IterationResult]

    @property
    def total_iterations(self) -> int:
        return len(self.param_values)

    @property
    def success(self) -> bool:
        return self.iteration_results[-1].success

    def __init__(
            self, target_block: str, target_param: str,
            param_values: List[Any]
    ):
        self.target_block = target_block
        self.target_param = target_param
        self.param_values = param_values
        self.iteration_results = []
