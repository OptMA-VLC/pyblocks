import abc
from typing import Any, List

from src.bdk.block_info import BlockInfo
from src.bdk.params.param_id import ParamId
from src.bdk.ports.port_id import PortId
from src.meow_sim.entity.block.available_parameter_entity import AvailableParameterEntity
from src.meow_sim.entity.block.port_entity import PortEntity


class IBlockRuntime(abc.ABC):
    @abc.abstractmethod
    def get_info(self) -> BlockInfo:
        pass

    @abc.abstractmethod
    def list_inputs(self, block_entity: 'BlockEntity') -> List[PortEntity]:
        pass

    @abc.abstractmethod
    def list_outputs(self, block_entity: 'BlockEntity') -> List[PortEntity]:
        pass

    @abc.abstractmethod
    def list_params(self) -> List[AvailableParameterEntity]:
        pass

    @abc.abstractmethod
    def set_parameter(self, param_id: ParamId, value: Any):
        pass

    @abc.abstractmethod
    def set_input(self, port_id: PortId, value: Any):
        pass

    @abc.abstractmethod
    def get_output(self, port_id: PortId):
        pass

    @abc.abstractmethod
    def run(self):
        pass
