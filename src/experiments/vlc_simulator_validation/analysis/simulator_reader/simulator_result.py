import numpy as np


class SimulatorResult:
    time: np.array
    signal: np.array

    def get_vpp(self) -> float:
        return max(self.signal) - min(self.signal)

    def get_v_half(self) -> float:
        return (max(self.signal) + min(self.signal))/2

    def trigger_at(self, voltage: float):
        idx = np.argmax(self.signal > voltage)
        trigger_time = self.time[idx]
        self.time = self.time - trigger_time

    def __sub__(self, other):
        res = SimulatorResult()
        res.time = self.time
        res.signal = self.signal - other.signal
        return res
