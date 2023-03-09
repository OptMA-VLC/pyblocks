from typing import List, Dict, Any

from src.bdk.params.param_id import ParamId
from src.bdk.ports.port_id import PortId
from src.meow_sim.entity.block.block import Block
from src.meow_sim.entity.connection import Connection
from src.meow_sim.entity.simulation.simulation_steps import SimulationStep
from src.meow_sim.logger import logger
from src.meow_sim.repository.signal_repository.signal_repository import SignalRepository


class SimulationUseCases:
    _signal_repo: SignalRepository

    def __init__(self, signal_repo: SignalRepository):
        self._signal_repo = signal_repo

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
        self._apply_inputs(block, step.inputs)
        self._run(block)
        self._extract_outputs(block, step.outputs)

    def _apply_params(self, block: Block, params: Dict[ParamId, Any]):
        try:
            for (param_id, value) in params.items():
                block.runtime.set_parameter(param_id, value)
        except Exception as ex:
            raise RuntimeError(
                f'Error applying parameters to Block {block.name} (instance_id: {block.instance_id})'
            ) from ex

    def _apply_inputs(self, block: Block, inputs: Dict[PortId, Connection]):
        try:
            for (port_id, conn) in inputs.items():
                signal = self._signal_repo.get(conn.id)
                block.runtime.set_input(port_id, signal)
        except Exception as ex:
            raise RuntimeError(
                f'Error applying inputs to Block {block.name} (instance_id: {block.instance_id})'
            ) from ex

    def _run(self, block: Block):
        try:
            block.runtime.run()
        except Exception as ex:
            raise RuntimeError(
                f'The block {block.name} (instance_id: {block.instance_id}) produce an error during its execution'
            ) from ex

    def _extract_outputs(self, block: Block, outputs: Dict[PortId, Connection]):
        try:
            for (port_id, conn) in outputs.items():
                out = block.runtime.get_output(port_id)
                self._signal_repo.set(conn.id, out)
        except Exception as ex:
            raise RuntimeError(
                f'Error extracting outputs from Block {block.name} (instance_id: {block.instance_id})'
            ) from ex
