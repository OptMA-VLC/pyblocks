from typing import Dict

from src.bdk.ports.port_id import PortId
from src.bdk.signals.signal import Signal


class InputBundle:
    _ports_and_signals: Dict[PortId, Signal]

    def __init__(self, ports_and_signals: Dict[PortId, Signal]):
        self._ports_and_signals = ports_and_signals

    def get(self, port: PortId) -> Signal:
        return self._ports_and_signals[port]
