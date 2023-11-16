import json
import pathlib
from dataclasses import dataclass, field
from typing import List


@dataclass
class LTSpiceRunnerConfig:
    input_signal_file: str
    schematic_file: pathlib.Path
    probe_signals: List[str]
    add_instructions: List[str] = field(default_factory=list)

    @staticmethod
    def from_path(path: pathlib.Path) -> 'LTSpiceRunnerConfig':
        with open(path) as f:
            json_dict = json.load(f)
            input_signal_file = json_dict['input_signal_file']
            schematic_file = pathlib.Path(json_dict['schematic_file'])
            probe_signals = json_dict['probe_signals']
            add_instructions = json_dict['add_instructions']

            return LTSpiceRunnerConfig(
                schematic_file=schematic_file,
                input_signal_file=input_signal_file,
                add_instructions=add_instructions,
                probe_signals=probe_signals
            )
