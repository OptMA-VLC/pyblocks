from typing import List

from src.pyblock_sim.entity.block.block_entity import BlockEntity
from src.pyblock_sim.entity.connection import Connection
from src.pyblock_sim.entity.graph.simulation_graph import SimulationGraph
from src.pyblock_sim.entity.simulation.simulation_steps import SimulationStep
from src.pyblock_sim.util.logger import logger
from src.pyblock_sim.repository.signal_repository.signal_repository import SignalRepository


class SimulationUseCases:
    _signal_repo: SignalRepository

    def __init__(self, signal_repo: SignalRepository):
        self._signal_repo = signal_repo

    def create_simulation_steps(self, graph: SimulationGraph) -> List[SimulationStep]:
        steps = []

        blocks_in_execution_order = graph.topological_sort()

        for block in blocks_in_execution_order:
            steps.append(SimulationStep(
                block=block,
                input_connections=graph.get_incoming_connections(block.instance_id),
            ))

        return steps

    def simulate(self, steps: List[SimulationStep]):
        logger.info('  ==== Running Simulation ====')
        try:
            for (i, step) in enumerate(steps):
                logger.info(f'Step {i+1}/{len(steps)} - Simulating Block {step.block.name}')
                self.simulate_step(step)
        except RuntimeError as ex:
            logger.error(ex)
            raise
        finally:
            logger.info('  ============================\n')

    def simulate_step(self, step: SimulationStep):
        block = step.block

        self._apply_params(block)
        self._apply_inputs(block, step.input_connections)
        self._run(block)
        self._extract_outputs(block)

    def _apply_params(self, block: BlockEntity):
        try:
            for param in block.user_params:
                block.runtime.set_parameter(param.param_id, param.value)
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
                f"The block '{block.name}' (instance_id: '{block.instance_id}') produced an error during its execution"
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
