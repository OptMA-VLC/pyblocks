from dataclasses import dataclass
from typing import Dict, List

from src.pyblock_sim.entity.project.command.command_entity import CommandEntity, CommandType
from src.pyblock_sim.entity.project.command.command_param_entity import CommandParamEntity
from src.pyblock_sim.entity.project.signal_selector import SignalSelector


@dataclass
class SaveCommandEntity(CommandEntity):
    # signals: List[SignalSelector]
    # save_path: str

    def __init__(self):
        super().__init__(CommandType.SAVE)

    def list_params(self) -> List[CommandParamEntity]:
        return [
            CommandParamEntity(param_id='save_path'),
            CommandParamEntity(param_id='signals', default=[])
        ]
