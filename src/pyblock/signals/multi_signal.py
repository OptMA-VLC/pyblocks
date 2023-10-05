from typing import Dict, Any, List
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
        try:
            return self._signals[signal_name]
        except KeyError:
            s = f"This MultiSignal object has no signal '{signal_name}'. Available signals are ["
            for name in self._signals.keys():
                s += f'{name}, '
            s = s[:-2] + ']\n'
            raise KeyError(s)

    def delete(self, signal_name: SignalName):
        del self._signals[signal_name]

    def list_signals(self) -> List[str]:
        signal_names = []
        for sig_name in self._signals.keys():
            signal_names.append(sig_name)
        return signal_names

    def __len__(self):
        return len(self._signals)

    def __str__(self):
        s = f"<{self.__class__} object at {id(self)}>\n"
        s += f"    {len(self)} signals:\n"
        for (name, signal) in self._signals.items():
            s += f"    '{name}' - {type(signal).__name__}\n"

        return s
