from typing import List

from src.pyblock_sim.entity.project.command.command_entity import CommandType, CommandEntity
from src.pyblock_sim.entity.project.command.command_param_entity import CommandParamEntity


class SimulateParamSweepCommandEntity(CommandEntity):
    def __init__(self):
        super().__init__(CommandType.SIMULATE_SWEEP)

    def list_params(self) -> List[CommandParamEntity]:
        return [
            CommandParamEntity(
                param_id='target_block_instance_id',
                description='Instance ID of the block where the parameter to sweep is located'
            ),
            CommandParamEntity(
                param_id='target_param_id',
                description='Parameter ID of the parameter to sweep'
            ),
            CommandParamEntity(
                param_id='steps',
                default=None,
                description='Number of steps over the sweep range'
            ),
            CommandParamEntity(
                param_id='start_value',
                default=None,
                description='Start value of the sweep range'
            ),
            CommandParamEntity(
                param_id='end_value',
                default=None,
                description='End value of the sweep range'
            ),
            CommandParamEntity(
                param_id='sweep_values',
                default=None,
                description="An array of values for the parameter to be swept."
                            "This parameter overrides 'start_value', 'end_value' and 'steps'"
            )
        ]
