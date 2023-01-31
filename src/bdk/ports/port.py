from typing import Type, Any

from src.bdk.ports.port_id import PortId


class Port:
    id: PortId
    signal_type: Type
    signal: Any

    def __init__(self, port_id: PortId, signal_type: Type):
        self.id = port_id
        self.signal_type = signal_type
