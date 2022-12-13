from dataclasses import dataclass, field
from typing import List

from .param_description import ParamDescription
from .port_description import PortDescription


@dataclass
class BlockDescription:
    id: str
    path: str
    params: List[ParamDescription] = field(default_factory=list)
    inputs: List[PortDescription] = field(default_factory=list)
    outputs: List[PortDescription] = field(default_factory=list)
