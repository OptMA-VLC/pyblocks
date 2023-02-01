from typing import List, Tuple, Any

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

    def apply_parameters(self, params: List[Tuple[ParamId, Any]]):
        for (param_id, value) in params:
            self._block_instance.params.set_param(param_id, value)

    def set_signal(self, port_id: PortId, value: Any):
        self._block_instance.inputs.set_signal(port_id, value)

    def get_signal(self, port_id: PortId):
        return self._block_instance.outputs.get_signal(port_id)

    def run(self):
        self._block_instance.run()
