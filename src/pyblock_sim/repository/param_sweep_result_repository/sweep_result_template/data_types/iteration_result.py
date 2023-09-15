from typing import Dict, Any


class IterationResult:
    signals: Dict[str, Any]
    iteration_number: int
    parameter_value: Any

    def get_signal(self, signal_name: str):
        try:
            return self.signals[signal_name]
        except KeyError:
            s = f"KeyError: Signal '{signal_name}' dos not exist. Available signals are: ["
            for name in self.signals.keys():
                s += f"'{name}', "
            s = s[:len(s)-2]
            s += ']'
            raise KeyError(s)
    def __str__(self):
        s =   'IterationResult object\n'
        s += f'Iteration number: {self.iteration_number}; Parameter value: {self.parameter_value}\n'
        s += f'Available signals:\n'
        for signal_name in self.signals.keys():
            s += f'  - {signal_name}\n'
        return s