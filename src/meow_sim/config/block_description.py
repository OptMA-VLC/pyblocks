from dataclasses import dataclass

from param_description import ParamDescription
from port_description import PortDescription


@dataclass
class BlockDescription:
    id: str = None
    path: str = None
    params: list[ParamDescription] = None
    inputs: list[PortDescription] = None
    outputs: list[PortDescription] = None
