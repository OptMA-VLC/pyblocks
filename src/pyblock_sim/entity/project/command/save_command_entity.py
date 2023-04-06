from dataclasses import dataclass
from typing import Dict, List

from src.pyblock_sim.entity.project.command.command_entity import CommandEntity, CommandType
from src.pyblock_sim.entity.project.signal_selector import SignalSelector


@dataclass
class SaveCommandEntity(CommandEntity):
    signals: List[SignalSelector]
    save_path: str

    @staticmethod
    def parse_args(args_json_dict: Dict) -> 'CommandEntity':
        save_path = args_json_dict.get('save_path', None)
        if save_path is None:
            raise ValueError(f"Can't parse save command because field 'save_path' is missing")

        signals_strs = args_json_dict.get('signals', [])
        signals = [SignalSelector.parse(s) for s in signals_strs]

        return SaveCommandEntity(
            type=CommandType.SAVE,
            signals=signals,
            save_path=save_path
        )
