import json
import pathlib
from dataclasses import dataclass, field
from typing import List


@dataclass
class LTSpiceRunnerConfig:
    file_name_in_circuit: str
    schematic_file: str
    probe_signals: List[str]
    add_instructions: List[str] = field(default_factory=list)

    @staticmethod
    def from_path(path: pathlib.Path) -> 'LTSpiceRunnerConfig':
        with open(path) as f:
            json_dict = json.load(f)
            file_name_in_circuit = json_dict['file_name_in_circuit']
            schematic_file = json_dict['schematic_file']
            probe_signals = json_dict['probe_signals']
            add_instructions = json_dict['add_instructions']

            return LTSpiceRunnerConfig(
                schematic_file=schematic_file,
                file_name_in_circuit=file_name_in_circuit,
                add_instructions=add_instructions,
                probe_signals=probe_signals
            )
