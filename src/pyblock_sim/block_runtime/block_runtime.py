import inspect
from typing import List, Any, Type

from src.pyblock.block.base_block import BaseBlock
from src.pyblock.block.block_distribution_id import BlockDistributionId
from src.pyblock.block.block_info import BlockInfo
from src.pyblock.block.params.param import Param
from src.pyblock.block.ports.input_port import InputPort
from src.pyblock.block.ports.output_port import OutputPort
from src.pyblock.block.ports.port_id import PortId
from src.pyblock.testing.validate_block import validate
from src.pyblock_sim.entity.block.block_entity import BlockEntity
from src.pyblock_sim.entity.block.interface_block_runtime import IBlockRuntime
from src.pyblock_sim.entity.block.parameter_entity import ParameterEntity
from src.pyblock_sim.entity.block.port_entity import PortEntity


class BlockRuntime(IBlockRuntime):
    distribution_id: BlockDistributionId
    _block_instance: BaseBlock

    _inputs: List[InputPort]
    _outputs: List[OutputPort]
    _params: List[Param]

    def __init__(self, block_class: Type[BaseBlock]):
        self._block_instance = block_class()
        validate(self._block_instance)

        self.distribution_id = self._block_instance.info.distribution_id
        self._inputs = self._find_inputs(self._block_instance)
        self._outputs = self._find_outputs(self._block_instance)
        self._params = self._find_params(self._block_instance)

    def get_info(self) -> BlockInfo:
        return self._block_instance.info

    def list_inputs(self, block_entity: BlockEntity) -> List[PortEntity]:
        return [
            PortEntity(block=block_entity, port_id=port.id, type=port.type)
            for port in self._inputs
        ]

    def list_outputs(self, block_entity: BlockEntity) -> List[PortEntity]:
        return [
            PortEntity(block=block_entity, port_id=port.id, type=port.type)
            for port in self._outputs
        ]

    def list_parameters(self) -> List[ParameterEntity]:
        return [
            ParameterEntity(param_id=param.id, type=param.type, value=None)
            for param in self._params
        ]

    def set_parameter(self, param: ParameterEntity):
        for block_param in self._params:
            if block_param.id == param.param_id:
                block_param.value = param.value
                return

        raise KeyError(f"No parameter with Id '{param.param_id}' in block '{self.distribution_id}'")

    def set_input(self, port_id: PortId, value: Any):
        for block_input in self._inputs:
            if block_input.id == port_id:
                block_input.signal = value
                return

        raise KeyError(f"No input port with Id '{port_id}' in block '{self.distribution_id}'")

    def get_output(self, port_id: PortId):
        for block_output in self._outputs:
            if block_output.id == port_id:
                return block_output.signal

        raise KeyError(f"No output port with Id '{port_id}' in block '{self.distribution_id}'")

    def run(self):
        self._block_instance.run()

    def _find_inputs(self, block: BaseBlock) -> List[InputPort]:
        return self._find_attributes(block, matching_type=InputPort)

    def _find_outputs(self, block: BaseBlock) -> List[OutputPort]:
        return self._find_attributes(block, matching_type=OutputPort)

    def _find_params(self, block: BaseBlock) -> List[Param]:
        return self._find_attributes(block, matching_type=Param)

    def _find_attributes(self, obj: object, matching_type=object) -> List:
        def check_is_attr(x):
            return not inspect.isroutine(x)

        members = inspect.getmembers(obj, check_is_attr)

        result = []
        for (_, attr) in members:
            if isinstance(attr, matching_type):
                result.append(attr)

        return result
