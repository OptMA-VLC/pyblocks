from typing import List, Optional

from src.pyblock_sim.use_case.simulate_use_case.simulation_step_report import SimulationStepReport


class SimulationReport:
    steps: List[SimulationStepReport]

    def __init__(self):
        self.steps = []

    @property
    def success(self):
        successes = [step.success for step in self.steps]
        return successes.count(False) == 0

    @property
    def exception(self) -> Optional[Exception]:
        if self.success or len(self.steps) == 0:
            return None
        return self.steps[-1].exception
