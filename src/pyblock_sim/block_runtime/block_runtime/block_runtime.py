from typing import List, Any

from src.pyblock.block.base_block import BaseBlock
from src.pyblock.block.block_distribution_id import BlockDistributionId
from src.pyblock.block.block_info import BlockInfo
from src.pyblock.block.params.param import ParamId
from src.pyblock.block.ports.port_id import PortId
from src.pyblock_sim.entity.block.block_entity import BlockEntity
from src.pyblock_sim.entity.block.interface_block_runtime import IBlockRuntime
from src.pyblock_sim.entity.block.parameter_entity import ParameterEntity
from src.pyblock_sim.entity.block.port_entity import PortEntity


class BlockRuntime(IBlockRuntime):
    distribution_id: BlockDistributionId
    _block_instance: BaseBlock

    def __init__(self, block_class: BaseBlock):
        self._block_instance = block_class()
        self.distribution_id = self._block_instance.block_info.distribution_id

    def get_info(self) -> BlockInfo:
        return self._block_instance.block_info

    def list_inputs(self, block_entity: BlockEntity) -> List[PortEntity]:
        return [
            PortEntity(block=block_entity, port_id=port.id, type=port.type)
            for port in self._block_instance.inputs
        ]

    def list_outputs(self, block_entity: BlockEntity) -> List[PortEntity]:
        return [
            PortEntity(block=block_entity, port_id=port.id, type=port.type)
            for port in self._block_instance.outputs
        ]

    def list_parameters(self) -> List[ParameterEntity]:
        return [
            ParameterEntity(param_id=param.id, type=param.type, value=None)
            for param in self._block_instance.params
        ]

    def set_parameter(self, param: ParameterEntity):
        block_params = self._block_instance.params

        for block_param in block_params:
            if block_param.id == param.param_id:
                block_param.value = param.value
                return

        raise KeyError(f"No parameter with Id '{param.param_id}' in block '{self.distribution_id}'")

    def set_input(self, port_id: PortId, value: Any):
        for input in self._block_instance.inputs:
            if input.id == port_id:
                input.signal = value
                return

        raise KeyError(f"No input port with Id '{port_id}' in block '{self.distribution_id}'")

    def get_output(self, port_id: PortId):
        for output in self._block_instance.outputs:
            if output.id == port_id:
                return output.signal

        raise KeyError(f"No output port with Id '{port_id}' in block '{self.distribution_id}'")

    def run(self):
        self._block_instance.run()
