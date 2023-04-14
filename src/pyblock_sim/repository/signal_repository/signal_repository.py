import copy
from logging import Logger
from typing import Any, Dict, Tuple

from src.pyblock.block.ports.port_id import PortId
from src.pyblock.signals.multi_signal import MultiSignal
from src.pyblock_sim.entity.block.block_instance_id import BlockInstanceId
from src.pyblock_sim.entity.project.signal_selector import SignalSelector
from src.pyblock_sim.util.logger_provider import LoggerProvider


class SignalRepository:
    _signals: Dict[Tuple[BlockInstanceId, PortId], Any]
    _logger: Logger

    def __init__(self, logger: Logger = None):
        self._signals = {}

        if logger is None:
            self._logger = LoggerProvider.get_logger()
        else:
            self._logger = logger

    def set(self, block_instance_id: BlockInstanceId, port_id: PortId, signal: Any):
        self._signals[(block_instance_id, port_id)] = signal

    def get(self, block_instance_id: BlockInstanceId, port_id: PortId) -> Any:
        try:
            return copy.deepcopy(self._signals[(block_instance_id, port_id)])
        except KeyError:
            raise KeyError(f"No signal exists for (block_instance: '{block_instance_id}', port: '{port_id}')")

    def get_by_selector(self, selector: SignalSelector):
        signal = self.get(selector.block, selector.port)

        if selector.signal_name is None:
            return signal

        if not isinstance(signal, MultiSignal):
            self._logger.warning(
                f"Attempt to access signal '{selector}' but target port does not contain a "
                f"{MultiSignal.__name__} instance. Ignoring the signal name and returning the "
                f"available signal, of tyṕe {type(signal).__name__}"
            )
            return signal

        return signal.get(selector.signal_name)
