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
        return copy.deepcopy(self._signals[connection_id])
