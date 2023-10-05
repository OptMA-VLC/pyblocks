from abc import ABC, abstractmethod
from typing import List

from src.pyblock_sim.entity.graph.simulation_graph import SimulationGraph
from src.pyblock_sim.entity.simulation.simulation_report import SimulationReport
from src.pyblock_sim.entity.simulation.simulation_step_report import SimulationStepReport
from src.pyblock_sim.entity.simulation.simulation_steps import SimulationStep


class SimulationProgressCallbacks(ABC):
    @abstractmethod
    def will_start_simulation(self):
        pass

    @abstractmethod
    def will_build_simulation_graph(self):
        pass

    @abstractmethod
    def did_build_simulation_graph(self, simulation_graph: SimulationGraph):
        pass

    @abstractmethod
    def will_calculate_steps(self):
        pass

    @abstractmethod
    def did_calculate_steps(self, simulation_steps: List[SimulationStep]):
        pass

    @abstractmethod
    def will_simulate_step(self):
        pass

    @abstractmethod
    def did_simulate_step(self, step_report: SimulationStepReport):
        pass

    @abstractmethod
    def did_complete_simulation(self, simulation_report: SimulationReport):
        pass
