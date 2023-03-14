from typing import List, Dict, Any, Tuple

import networkx.algorithms.dag

from src.bdk.params.param_id import ParamId
from src.bdk.ports.port_id import PortId
from src.meow_sim.entity.block.block_entity import BlockEntity
from src.meow_sim.entity.block.block_instance_id import BlockInstanceId
from src.meow_sim.entity.connection import Connection
from src.meow_sim.entity.graph.simulation_graph import SimulationGraph
from src.meow_sim.entity.simulation.simulation_steps import SimulationStep
from src.meow_sim.logger import logger
from src.meow_sim.repository.signal_repository.signal_repository import SignalRepository


class SimulationUseCases:
    _signal_repo: SignalRepository

    def __init__(self, signal_repo: SignalRepository):
        self._signal_repo = signal_repo

    def create_simulation_steps(
            self, graph: SimulationGraph,
    ) -> List[SimulationStep]:
        steps = []
        for block in graph.topological_sort():

            steps.append(SimulationStep(
                block=block,
                params={},  # TODO: implement params
                input_connections=graph.get_incoming_connections(block.instance_id),
            ))

        return steps

    def simulate(self, steps: List[SimulationStep]):
        logger.info('\n==== Running Simulation ====\n')
        try:
            for (i, step) in enumerate(steps):
                logger.info(f'Step {i+1}/{len(steps)} - Simulating Block {step.block.name}')
                self.simulate_step(step)
        except RuntimeError as ex:
            logger.error(ex)
            raise
        finally:
            logger.info('\n============================\n')

    def simulate_step(self, step: SimulationStep):
        block = step.block

        self._apply_params(block, step.params)
        self._apply_inputs(block, step.input_connections)
        self._run(block)
        self._extract_outputs(block)

    def _apply_params(self, block: BlockEntity, params: Dict[ParamId, Any]):
        try:
            for (param_id, value) in params.items():
                block.runtime.set_parameter(param_id, value)
        except Exception as ex:
            raise RuntimeError(
                f'Error applying parameters to Block {block.name} (instance_id: {block.instance_id})'
            ) from ex

    def _apply_inputs(self, block: BlockEntity, input_connections: List[Connection]):
        for conn in input_connections:
            try:
                signal = self._signal_repo.get(conn.from_port.instance_id)
                block.runtime.set_input(conn.to_port.port_id, signal)
            except Exception as ex:
                raise RuntimeError(
                    f"Error transferring signal from port '{conn.from_port.instance_id}' to port '{conn.to_port.instance_id}'"
                ) from ex

    def _run(self, block: BlockEntity):
        try:
            block.runtime.run()
        except Exception as ex:
            raise RuntimeError(
                f'The block {block.name} (instance_id: {block.instance_id}) produce an error during its execution'
            ) from ex

    def _extract_outputs(self, block: BlockEntity):
        for output_port in block.outputs:
            try:
                output_signal = block.runtime.get_output(output_port.port_id)
                self._signal_repo.set(output_port.instance_id, output_signal)
            except Exception as ex:
                raise RuntimeError(
                    f"Error extracting outputs from PortEntity '{output_port.instance_id}'"
                ) from ex
