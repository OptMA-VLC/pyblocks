from typing import Dict

from src.pyblock_sim.entity.project.command.command_entity import CommandEntity, CommandType
from src.pyblock_sim.entity.project.command.plot_command_entity import PlotCommandEntity
from src.pyblock_sim.entity.project.command.save_command_entity import SaveCommandEntity


class CommandParser:
    @staticmethod
    def parse(command_json_dict: Dict) -> CommandEntity:
        cmd = command_json_dict.get('command', None)
        args = command_json_dict.get('args', {})

        if cmd is None:
            raise ValueError("Missing required field 'command'")

        if cmd == CommandType.PLOT.value:
            return PlotCommandEntity.parse_args(args)
        elif cmd == CommandType.SAVE.value:
            return SaveCommandEntity.parse_args(args)
        else:
            raise ValueError(f"The command '{cmd}' is not a valid command")
