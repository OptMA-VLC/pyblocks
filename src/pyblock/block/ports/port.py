from typing import Type, Any

from src.pyblock.block.ports.port_id import PortId


class Port:
    id: PortId
    type: Type
    signal: Any

    def __init__(self, port_id: str, type: Type = Any):
        self.id = PortId(port_id)
        self.type = type
        self.signal = None
