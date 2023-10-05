from typing import List

from src.pyblock_sim.entity.graph.simulation_graph import SimulationGraph
from src.pyblock_sim.entity.simulation.simulation_steps import SimulationStep


class ComputeSimulationStepsUseCase:
    def compute_simulation_steps(self, graph: SimulationGraph) -> List[SimulationStep]:
        steps = []

        blocks_in_execution_order = graph.topological_sort()

        for block in blocks_in_execution_order:
            incoming_connections = graph.get_incoming_connections(block.instance_id)
            steps.append(SimulationStep(
                block=block, input_connections=incoming_connections,
            ))

        return steps
