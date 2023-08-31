from typing import Type, Any

from src.pyblock.block.ports.port_id import PortId


class Port:
    id: PortId
    type: Type
    signal: Any
    description: str

    def __init__(
            self,
            port_id: str,
            type: Type = Any,
            description: str = '',
    ):
        self.id = PortId(port_id)
        self.type = type
        self.signal = None
        self.description = description
