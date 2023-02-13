from dataclasses import dataclass, field
from typing import List


@dataclass
class LTSpiceRunnerConfig:
    file_name_in_circuit: str
    schematic_file: str
    probe_signals: List[str]
    add_instructions: List[str] = field(default_factory=list)
