from typing import List

from src.pyblock_sim.entity.graph.simulation_graph import SimulationGraph
from src.pyblock_sim.entity.simulation.simulation_report import SimulationReport
from src.pyblock_sim.entity.simulation.simulation_step_report import SimulationStepReport
from src.pyblock_sim.entity.simulation.simulation_steps import SimulationStep
from src.pyblock_sim.use_case.simulate_use_case.simulation_progress_callbacks import SimulationProgressCallbacks


class EmptySimulationProgressCallbacks(SimulationProgressCallbacks):

    def will_start_simulation(self):
        pass

    def will_build_simulation_graph(self):
        pass

    def did_build_simulation_graph(self, simulation_graph: SimulationGraph):
        pass

    def will_calculate_steps(self):
        pass

    def did_calculate_steps(self, simulation_steps: List[SimulationStep]):
        pass

    def will_simulate_step(self):
        pass

    def did_simulate_step(self, step_report: SimulationStepReport):
        pass

    def did_complete_simulation(self, simulation_report: SimulationReport):
        pass
