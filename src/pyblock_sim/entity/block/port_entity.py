from dataclasses import dataclass
from typing import Type, Any

from src.pyblock.block.ports.port_id import PortId


@dataclass
class PortEntity:
    block: 'BlockEntity'
    port_id: PortId
    type: Type = Any
