from typing import List, Tuple, Any, Dict

from src.bdk.base_block import BaseBlock
from src.bdk.block_distribution_id import BlockDistributionId
from src.bdk.block_info import BlockInfo
from src.bdk.params.parameter import ParamId
from src.bdk.ports.port_id import PortId


class BlockAdapter:
    distribution_id: BlockDistributionId
    _block_instance: BaseBlock

    def __init__(self, block_class: BaseBlock):
        self._block_instance = block_class()
        self.distribution_id = self._block_instance.block_info.distribution_id

    def get_info(self) -> BlockInfo:
        return self._block_instance.block_info

    def apply_parameters(self, params: Dict[ParamId, Any]):
        block_params = self._block_instance.params

        for (param_id, value) in params.items():
            for block_param in block_params:
                if block_param.id == param_id:
                    block_param.value = value

    def set_input(self, port_id: PortId, value: Any):
        for input in self._block_instance.inputs:
            if input.id == port_id:
                input.signal = value
                return

        raise KeyError(f'No input port with Id {port_id} in block {self.distribution_id}')

    def get_output(self, port_id: PortId):
        for output in self._block_instance.outputs:
            if output.id == port_id:
                return output.signal

        raise KeyError(f'No output port with Id {port_id} in block {self.distribution_id}')

    def run(self):
        self._block_instance.run()
