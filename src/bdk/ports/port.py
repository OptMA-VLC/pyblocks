from typing import Type, Any

from src.bdk.ports.port_id import PortId


class Port:
    id: PortId
    type: Type
    signal: Any

    def __init__(self, port_id: str, type: Type):
        self.id = PortId(port_id)
        self.type = type
        self.signal = None

    # TODO: enforce type consistency when assigning to signal
