from dataclasses import dataclass
from typing import List, Optional, Dict

from src.pyblock_sim.entity.project.command.command_entity import CommandEntity, CommandType
from src.pyblock_sim.entity.project.command.command_param_entity import CommandParamEntity
from src.pyblock_sim.entity.project.signal_selector import SignalSelector


class PlotCommandEntity(CommandEntity):
    # signals: List[SignalSelector]
    # save_path: Optional[str]

    def __init__(self):
        super().__init__(CommandType.PLOT)

    def list_params(self) -> List[CommandParamEntity]:
        return [
            CommandParamEntity(param_id='signals', default=[]),
            CommandParamEntity(param_id='save_path', default=None)
        ]
