import abc
from typing import Any, List

from src.pyblock.block.block_info import BlockInfo
from src.pyblock.block.params.param_id import ParamId
from src.pyblock.block.ports.port_id import PortId
from src.pyblock_sim.entity.block.parameter_entity import ParameterEntity
from src.pyblock_sim.entity.block.port_entity import PortEntity


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
    def list_parameters(self) -> List[ParameterEntity]:
        pass

    @abc.abstractmethod
    def set_parameter(self, param: ParameterEntity):
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
