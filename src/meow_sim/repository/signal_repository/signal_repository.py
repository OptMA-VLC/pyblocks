import copy
from typing import Any, Dict

from src.meow_sim.entity.block.port_instance_id import PortInstanceId
from src.meow_sim.entity.connection_id import ConnectionId


class SignalRepository:
    _signals: Dict[PortInstanceId, Any]

    def __init__(self):
        self._signals = {}

    def set(self, port_instance_id: PortInstanceId, signal: Any):
        self._signals[port_instance_id] = signal

    def get(self, port_instance_id: PortInstanceId) -> Any:
        try:
            return copy.deepcopy(self._signals[port_instance_id])
        except KeyError:
            raise KeyError(f"No signal exists for port_instance_id '{port_instance_id}'")
