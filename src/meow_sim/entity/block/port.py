from dataclasses import dataclass
from typing import Type, Any

from src.bdk.ports.port_id import PortId


@dataclass
class Port:
    block: 'Block'
    port_id: PortId
    type: Type = Any
