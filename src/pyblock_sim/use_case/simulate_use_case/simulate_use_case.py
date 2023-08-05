import contextlib
import io
import time
from typing import List

from src.pyblock_sim.entity.block.block_entity import BlockEntity
from src.pyblock_sim.entity.graph.connection_entity import ConnectionEntity
from src.pyblock_sim.entity.project.project_entity import ProjectEntity
from src.pyblock_sim.entity.simulation.simulation_steps import SimulationStep
from src.pyblock_sim.repository.block_repository.block_repository import BlockRepository
from src.pyblock_sim.repository.path_manager.path_manager import PathManager
from src.pyblock_sim.repository.signal_repository.signal_repository import SignalRepository

from src.pyblock_sim.use_case.build_simulation_graph.build_simulation_graph_use_case import BuildSimulationGraphUseCase
from src.pyblock_sim.use_case.compute_simulation_steps.compute_simulation_steps_use_case import \
    ComputeSimulationStepsUseCase
from src.pyblock_sim.use_case.simulate_use_case.empty_simulation_progress_callbacks import \
    EmptySimulationProgressCallbacks
from src.pyblock_sim.use_case.simulate_use_case.simulation_exceptions import BlockParamException, BlockInputException, \
    BlockRunningException, BlockOutputException
from src.pyblock_sim.use_case.simulate_use_case.simulation_progress_callbacks import SimulationProgressCallbacks
from src.pyblock_sim.use_case.simulate_use_case.simulation_report import SimulationReport
from src.pyblock_sim.use_case.simulate_use_case.simulation_step_report import SimulationStepReport
from src.pyblock_sim.util.set_directory import set_directory


class SimulateUseCase:
    _signal_repo: SignalRepository
    _block_repo: BlockRepository
    _path_manager: PathManager

    def __init__(
            self,
            signal_repo: SignalRepository,
            block_repo: BlockRepository,
            path_manager: PathManager
    ):
        self._signal_repo = signal_repo
        self._block_repo = block_repo
        self._path_manager = path_manager

    def simulate(
            self, project: ProjectEntity,
            progress_callback: SimulationProgressCallbacks = EmptySimulationProgressCallbacks()
    ) -> SimulationReport:
        report = SimulationReport()
        progress_callback.will_start_simulation()

        build_graph_use_case = BuildSimulationGraphUseCase(self._block_repo)
        compute_simulation_steps_use_case = ComputeSimulationStepsUseCase()

        progress_callback.will_build_simulation_graph()
        simulation_graph = build_graph_use_case.build_simulation_graph(project.graph_spec)
        progress_callback.did_build_simulation_graph(simulation_graph)

        progress_callback.will_calculate_steps()
        simulation_steps = compute_simulation_steps_use_case.compute_simulation_steps(simulation_graph)
        progress_callback.did_calculate_steps(simulation_steps)

        step_count = 0
        for step in simulation_steps:
            progress_callback.will_simulate_step()

            step_report = self._simulate_step(step)
            step_report.total_number_of_steps = len(simulation_steps)
            step_report.step_number = step_count
            step_count += 1

            report.steps.append(step_report)
            progress_callback.did_simulate_step(step_report)
            if not step_report.success:
                break

        progress_callback.did_complete_simulation(report)
        return report

    def _simulate_step(self, step: SimulationStep) -> SimulationStepReport:
        project_path = self._path_manager.get_project_absolute_path()
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

            with set_directory(project_path.parent):
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
