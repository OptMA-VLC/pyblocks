from typing import Any

from src.bdk.ports.port import Port
from src.bdk.ports.port_id import PortId


class PortBundle(dict):
    def __init__(self, *args):
        port_dict = {}

        for arg in args:
            if isinstance(arg, Port):
                port_dict[arg.id] = arg
            else:
                assert TypeError('Port Bundle constructor takes Port objects as arguments')

        super().__init__(port_dict)

    def get_signal(self, port_id: PortId) -> Any:
        port = self[port_id]
        return port.signal

    def set_signal(self, port_id: PortId, signal: Any):
        port = self[port_id]
        port.signal = signal
