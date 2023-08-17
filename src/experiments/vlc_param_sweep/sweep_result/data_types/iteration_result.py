from typing import Dict, Any


class IterationResult:
    signals: Dict[str, Any]
    iteration_number: int
    parameter_value: Any

    def get_signal(self, signal_name: str):
        return self.signals[signal_name]

    def __str__(self):
        s =   'IterationResult object\n'
        s += f'Iteration number: {self.iteration_number}; Parameter value: {self.parameter_value}\n'
        s += f'Available signals:\n'
        for signal_name in self.signals.keys():
            s += f'  - {signal_name}\n'
        return s