from abc import abstractmethod, ABC

from .block_info import BlockInfo
from .params.parameter import Parameter
from .port import Port
from .signals.signal import Signal


class BaseBlock:
    @abstractmethod
    def get_info(self) -> BlockInfo:
        pass

    @abstractmethod
    def validate_inputs(self, inputs: [(Port, Signal)]):
        pass

    @abstractmethod
    def run(self, inputs: [(Port, Signal)], params: [Parameter]) -> [(Port, Signal)]:
        pass
