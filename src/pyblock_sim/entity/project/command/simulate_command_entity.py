from typing import List

from src.pyblock_sim.entity.project.command.command_entity import CommandEntity, CommandType
from src.pyblock_sim.entity.project.command.command_param_entity import CommandParamEntity


class SimulateCommandEntity(CommandEntity):
    def __init__(self):
        super().__init__(CommandType.SIMULATE)

    def list_params(self) -> List[CommandParamEntity]:
        return []
