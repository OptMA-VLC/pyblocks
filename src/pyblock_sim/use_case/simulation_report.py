from typing import List

from src.pyblock_sim.use_case.simulation_step_report import SimulationStepReport


class SimulationReport:
    steps: List[SimulationStepReport]

    def __init__(self):
        self.steps = []

    @property
    def success(self):
        successes = [step.success for step in self.steps]
        return successes.count(False) == 0
