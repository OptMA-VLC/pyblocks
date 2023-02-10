from dataclasses import dataclass
from typing import List


@dataclass
class LTSpiceRunnerConfig:
    file_name_input: str
    file_name_output: str
    file_name_in_circuit: str
    ltspice_file_relative_path: str
    ltspice_file_name: str
    add_instructions: List[str]
    probe_signals: List[str]

    @staticmethod
    def from_json(json_config):
        return LTSpiceRunnerConfig(
            file_name_input=json_config['file_name_input'],
            file_name_output=json_config['file_name_output'],
            file_name_in_circuit=json_config['file_name_in_circuit'],
            ltspice_file_relative_path=json_config['ltspice_file_relative_path'],
            ltspice_file_name=json_config['ltspice_file_name'],
            add_instructions=json_config['add_instructions'],
            probe_signals=json_config['probe_signals']
        )
