from abc import ABC, abstractmethod
from typing import Any

from src.bdk.block_info import BlockInfo
from src.bdk.params.param_id import ParamId
from src.bdk.ports.port_id import PortId


class IBlockRuntime(ABC):
    @abstractmethod
    def get_info(self) -> BlockInfo:
        pass

    @abstractmethod
    def set_parameter(self, param_id: ParamId, value: Any):
        pass

    @abstractmethod
    def set_input(self, port_id: PortId, value: Any):
        pass

    @abstractmethod
    def get_output(self, port_id: PortId):
        pass

    @abstractmethod
    def run(self):
        pass
