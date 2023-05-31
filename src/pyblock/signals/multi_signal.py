from typing import Dict, Any
from src.pyblock.signals.signal_name import SignalName


class MultiSignal:
    _signals: Dict

    def __init__(self, values=None):
        self._signals = {}

        if isinstance(values, Dict):
            for (key, value) in values.items():
                self._signals[SignalName(key)] = value

    def set(self, signal_name: SignalName, signal: Any):
        self._signals[signal_name] = signal

    def get(self, signal_name: SignalName):
        return self._signals[signal_name]

    def delete(self, signal_name: SignalName):
        del self._signals[signal_name]

    def __len__(self):
        return len(self._signals)

    def __str__(self):
        s = f"<{self.__class__} object at {id(self)}>\n"
        s += f"    {len(self)} signals:\n"
        for (name, signal) in self._signals.items():
            s += f"    '{name}' - {type(signal).__name__}\n"

        return s
