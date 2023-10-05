from typing import List, Any

from .iteration_result import IterationResult


class SweepResult:
    param_values: List[Any]
    target_block: str
    target_param: str

    iterations: List[IterationResult]

    @property
    def num_iterations(self) -> int:
        return len(self.iterations)

    def get_signals(self, signal_name: str) -> List:
        signals = []
        for iter_result in self.iterations:
            signals.append(iter_result.get_signal(signal_name))
        return signals

    def __str__(self):
        s =  f'SweepResult object\n'
        s += f'  > Target Block: {self.target_block}\n'
        s += f'  > Target Parameter: {self.target_param}\n'
        s += f'  > Num iterations: {self.num_iterations}\n'
        s += f'  > Parameter Values: {self.param_values}\n'
        return s