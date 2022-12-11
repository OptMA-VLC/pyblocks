from dataclasses import dataclass, field
from typing import List

from src.meow_sim.config.param_description import ParamDescription
from src.meow_sim.config.port_description import PortDescription


@dataclass
class BlockDescription:
    id: str
    path: str
    params: List[ParamDescription] = field(default_factory=list)
    inputs: List[PortDescription] = field(default_factory=list)
    outputs: List[PortDescription] = field(default_factory=list)
