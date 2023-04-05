from dataclasses import dataclass
from pathlib import Path
from typing import List, Optional, Dict

from src.pyblock_sim.entity.project.command.command_entity import CommandEntity, CommandType
from src.pyblock_sim.entity.project.signal_selector import SignalSelector


@dataclass
class PlotCommandEntity(CommandEntity):
    signals: List[SignalSelector]
    save_path: Optional[Path]

    @staticmethod
    def parse_args(args_json_dict: Dict) -> 'PlotCommandEntity':
        signals_list = args_json_dict.get('signals', [])
        if not isinstance(signals_list, List):
            ValueError("Field 'signals' in plot command must be a list")

        parsed_signals = []
        for signal in signals_list:
            parsed_signals.append(SignalSelector.parse(signal))

        save_path = args_json_dict.get('save_path', None)

        return PlotCommandEntity(
            type=CommandType.PLOT,
            signals=parsed_signals,
            save_path=save_path
        )

