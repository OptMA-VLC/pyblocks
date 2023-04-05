import copy
from typing import Any, Dict, Tuple

from src.pyblock.block.ports.port_id import PortId
from src.pyblock_sim.entity.block.block_instance_id import BlockInstanceId


class SignalRepository:
    _signals: Dict[Tuple[BlockInstanceId, PortId], Any]

    def __init__(self):
        self._signals = {}

    def set(self, block_instance_id: BlockInstanceId, port_id: PortId, signal: Any):
        self._signals[(block_instance_id, port_id)] = signal

    def get(self, block_instance_id: BlockInstanceId, port_id: PortId) -> Any:
        try:
            return copy.deepcopy(self._signals[(block_instance_id, port_id)])
        except KeyError:
            raise KeyError(f"No signal exists for (block_instance: '{block_instance_id}', port: '{port_id}')")
