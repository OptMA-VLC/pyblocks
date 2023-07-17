import contextlib
import io
import time
from typing import List

from src.pyblock_sim.entity.block.block_entity import BlockEntity
from src.pyblock_sim.entity.graph.connection_entity import ConnectionEntity
from src.pyblock_sim.entity.simulation.simulation_steps import SimulationStep
from src.pyblock_sim.repository.path_manager.path_manager import PathManager
from src.pyblock_sim.repository.signal_repository.signal_repository import SignalRepository
from src.pyblock_sim.use_case.simulate.simulation_exceptions import BlockInputException, BlockParamException, \
    BlockOutputException, BlockRunningException
from src.pyblock_sim.use_case.simulate.simulation_report import SimulationReport
from src.pyblock_sim.use_case.simulate.simulation_step_report import SimulationStepReport
from src.pyblock_sim.util.set_directory import set_directory


class SimulateUseCase:
    _signal_repo: SignalRepository
    _path_manager: PathManager

    def __init__(self, signal_repo: SignalRepository, path_manager: PathManager):
        self._signal_repo = signal_repo
        self._path_manager = path_manager

    def simulate(self, steps: List[SimulationStep]) -> SimulationReport:
        report = SimulationReport()
        project_path = self._path_manager.get_project_absolute_path()

        with set_directory(project_path.parent):
            for step in steps:
                step_report = self.simulate_step(step)
                report.steps.append(step_report)
                if not step_report.success:
                    break

        return report

    def simulate_step(self, step: SimulationStep) -> SimulationStepReport:
        block = step.block

        report = SimulationStepReport(block.instance_id)
        report.success = True
        start_time = None
        stop_time = None
        stdout = ''
        stderr = ''

        try:
            self._apply_params(block)
            self._apply_inputs(block, step.input_connections)

            start_time = time.perf_counter()
            (stdout, stderr) = self._run(block)
            stop_time = time.perf_counter()

            self._extract_outputs(block)
        except Exception as ex:
            report.exception = ex
            report.success = False

        if start_time is not None and stop_time is not None:
            report.execution_time = stop_time - start_time
        report.stdout = stdout
        report.stderr = stderr

        return report

    def _apply_params(self, block: BlockEntity):
        for param in block.param_manager.get_params():
            try:
                block.runtime.set_parameter(param)
            except Exception as ex:
                raise BlockParamException(block.instance_id, param.param_id, ex)

    def _apply_inputs(self, block: BlockEntity, input_connections: List[ConnectionEntity]):
        for conn in input_connections:
            try:
                signal = self._signal_repo.get_by_selector(conn.origin)
                block.runtime.set_input(conn.destination.port, signal)
            except Exception as ex:
                raise BlockInputException(conn, ex)

    def _run(self, block: BlockEntity) -> (io.StringIO, io.StringIO):
        try:
            with contextlib.redirect_stdout(io.StringIO()) as out_stream:
                with contextlib.redirect_stderr(io.StringIO()) as err_stream:
                    block.runtime.run()
        except Exception as ex:
            raise BlockRunningException(block.instance_id, ex)

        stdout = out_stream.getvalue()
        stderr = err_stream.getvalue()

        return stdout, stderr

    def _extract_outputs(self, block: BlockEntity):
        for output_port in block.outputs:
            try:
                output_signal = block.runtime.get_output(output_port.port_id)
                self._signal_repo.set(
                    output_port.block.instance_id,
                    output_port.port_id,
                    output_signal
                )
            except Exception as ex:
                raise BlockOutputException(block.instance_id, output_port.port_id, ex)
