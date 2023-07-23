from typing import Dict

from src.pyblock_sim.entity.project.command.command_entity import CommandEntity, CommandType
from src.pyblock_sim.entity.project.command.plot_command_entity import PlotCommandEntity
from src.pyblock_sim.entity.project.command.save_command_entity import SaveCommandEntity


class CommandParser:
    @staticmethod
    def parse(command_json_dict: Dict) -> CommandEntity:
        json_cmd = command_json_dict.get('command', None)
        json_params_list = command_json_dict.get('parameters')

        if json_cmd is None:
            raise ValueError("Missing required field 'command'")

        cmd_entity = CommandParser._get_entity_from_command_string(json_cmd)

        if json_params_list is not None:
            for json_param in json_params_list:
                param_id = json_param.get('param_id')
                param_value = json_param.get('value')

                cmd_entity.set_param(param_id, param_value)

        unfulfilled_params = cmd_entity.list_unfulfilled_params()
        if len(unfulfilled_params) != 0:
            s = f"The following required parameters for command '{cmd_entity.type}' were not provided:\n"
            for param in unfulfilled_params:
                s += f"    '{param.id}'\n"
            raise ValueError(s)

        return cmd_entity

    @staticmethod
    def _get_entity_from_command_string(cmd_str: str) -> CommandEntity:
        command_classes = [
            PlotCommandEntity,
            SaveCommandEntity
        ]

        for cmd_class in command_classes:
            cmd_obj = cmd_class()
            if cmd_str == cmd_obj.type.value:
                return cmd_obj

        raise ValueError(f"The command '{cmd_str}' is not a valid command")
