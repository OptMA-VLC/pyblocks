import copy
from typing import Any, Dict

from src.meow_sim.entity.connection_id import ConnectionId


class SignalRepository:
    _signals: Dict[ConnectionId, Any]

    def __init__(self):
        self._signals = {}

    def set(self, connection_id: ConnectionId, signal: Any):
        self._signals[connection_id] = signal

    def get(self, connection_id: ConnectionId) -> Any:
        try:
            return copy.deepcopy(self._signals[connection_id])
        except KeyError:
            raise KeyError(f"No signal exists for connection_id '{connection_id}'")

