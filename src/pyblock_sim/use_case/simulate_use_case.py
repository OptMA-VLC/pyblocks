from typing import List

from src.pyblock_sim.entity.block.block_entity import BlockEntity
from src.pyblock_sim.entity.graph.connection_entity import ConnectionEntity
from src.pyblock_sim.entity.simulation.simulation_steps import SimulationStep
from src.pyblock_sim.repository.block_repository.interface_block_repository import IBlockRepository
from src.pyblock_sim.repository.signal_repository.signal_repository import SignalRepository
from src.pyblock_sim.util.logger import logger


class SimulateUseCase:
    _signal_repo: SignalRepository

    def __init__(
            self,
            signal_repository: SignalRepository,
            block_repository: IBlockRepository
    ):
        self._signal_repo = signal_repository
        self._block_repo = block_repository

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
            for param in block.param_manager.get_params():
                block.runtime.set_parameter(param)
        except Exception as ex:
            raise RuntimeError(
                f'Error applying parameters to Block {block.name} (instance_id: {block.instance_id})'
            ) from ex

    def _apply_inputs(self, block: BlockEntity, input_connections: List[ConnectionEntity]):
        for conn in input_connections:
            try:
                signal = self._signal_repo.get(conn.origin_block, conn.origin_port)
                block.runtime.set_input(conn.destination_port, signal)
            except Exception as ex:
                raise RuntimeError(
                    f"Error transferring signal from (block: '{conn.origin_block}', port: '{conn.origin_port}') "
                    f"to (block: '{conn.destination_block}', port: '{conn.destination_port})'"
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
                self._signal_repo.set(output_port.block.instance_id, output_port.port_id, output_signal)
            except Exception as ex:
                raise RuntimeError(
                    f"Error extracting outputs from PortEntity '{output_port.instance_id}'"
                ) from ex
