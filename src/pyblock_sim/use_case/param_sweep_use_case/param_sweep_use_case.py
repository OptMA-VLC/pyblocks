import copy
import numbers
from typing import List, Any

from src.pyblock_sim.entity.project.command.command_entity import CommandEntity
from src.pyblock_sim.entity.project.project_entity import ProjectEntity
from src.pyblock_sim.repository.block_repository.block_repository import BlockRepository
from src.pyblock_sim.repository.path_manager.path_manager import PathManager
from src.pyblock_sim.repository.signal_repository.signal_repository import SignalRepository
from src.pyblock_sim.use_case.param_sweep_use_case.empty_sweep_progress_callbacks import EmptySweepProgressCallbacks
from src.pyblock_sim.use_case.param_sweep_use_case.param_sweep_result import ParamSweepResult, IterationResult
from src.pyblock_sim.use_case.param_sweep_use_case.sweep_progress_callbacks import SweepProgressCallbacks
from src.pyblock_sim.use_case.simulate_use_case.simulate_use_case import SimulateUseCase


class ParamSweepUseCase:
    _signal_repo: SignalRepository
    _block_repo: BlockRepository
    _path_manager: PathManager

    def __init__(
            self, signal_repo: SignalRepository,
            block_repo: BlockRepository,
            path_manager: PathManager
    ):
        self._signal_repo = signal_repo
        self._block_repo = block_repo
        self._path_manager = path_manager

    def simulate_sweep(
            self,
            command: CommandEntity,
            project: ProjectEntity,
            sweep_progress_callbacks: SweepProgressCallbacks = EmptySweepProgressCallbacks()
    ):
        sweep_progress_callbacks.will_start_sweep()

        sweep_values = self._get_sweep_values(command)
        sweep_result = ParamSweepResult(
            target_block=command.get_param('target_block_instance_id'),
            target_param=command.get_param('target_param_id'),
            param_values=sweep_values
        )
        project = copy.deepcopy(project)

        iteration = 0
        for param_value in sweep_values:
            sweep_progress_callbacks.will_start_iteration(iteration, len(sweep_values), param_value)

            iteration_result = self._simulate_iteration(
                command, project, iteration, param_value
            )

            sweep_result.iteration_results.append(iteration_result)
            iteration += 1
            sweep_progress_callbacks.did_finish_iteration(iteration_result)

            if not iteration_result.success:
                sweep_progress_callbacks.did_finish_sweep(sweep_result)
                raise iteration_result.report.exception

        sweep_progress_callbacks.did_finish_sweep(sweep_result)

        return sweep_result

    def _simulate_iteration(
            self, command: CommandEntity, project: ProjectEntity,
            iteration: int, param_value: Any
    ) -> IterationResult:
        signal_repo = SignalRepository()
        simulate_use_case = SimulateUseCase(
            signal_repo=signal_repo,
            block_repo=self._block_repo,
            path_manager=self._path_manager
        )

        self._apply_param_on_project(project, command, param_value)
        report = simulate_use_case.simulate(project)

        iteration_result = IterationResult(
            iteration_number=iteration, iteration_value=param_value,
            report=report, signal_repo=signal_repo
        )

        return iteration_result

    def _get_sweep_values(self, command: CommandEntity) -> List[Any]:
        sweep_values = command.get_param('sweep_values')
        start_value = command.get_param('start_value')
        end_value = command.get_param('end_value')
        steps = command.get_param('steps')

        if sweep_values is not None:
            if not isinstance(sweep_values, List):
                raise ValueError(f"Parameter 'sweep_values' must be a List but is {sweep_values}")
            return sweep_values

        if not isinstance(start_value, numbers.Complex):
            # check against numbers.Complex because int and float are subclasses
            raise ValueError(f"Parameter 'start_value' must be a number but is {start_value}")

        if not isinstance(end_value, numbers.Complex):
            raise ValueError(f"Parameter 'end_value' must be a number but is {end_value}")

        if not isinstance(steps, int):
            raise ValueError(f"Parameter 'steps' must be an integer but is {steps}")
        if not steps >= 2:
            raise ValueError(f"Parameter 'steps' must be at least 2 but is {steps}")

        step_size = (end_value - start_value) / (steps - 1)
        sweep_values_arr = []
        for i in range(steps):
            sweep_values_arr.append(start_value + i * step_size)

        return sweep_values_arr

    def _apply_param_on_project(self, project: ProjectEntity, command: CommandEntity, value: Any):
        target_block_id = command.get_param('target_block_instance_id')
        target_param_id = command.get_param('target_param_id')

        target_block = None
        target_param = None
        for block in project.graph_spec.blocks:
            if block.instance_id == target_block_id:
                target_block = block

        if target_block is None:
            raise KeyError(f"Could not find the block '{target_block_id}' in simulation graph")

        for param in target_block.params:
            if param.param_id == target_param_id:
                target_param = param

        if target_param is None:
            raise KeyError(f"Could not find param '{target_param_id}' in block '{target_block_id}'")

        target_param.value = value

