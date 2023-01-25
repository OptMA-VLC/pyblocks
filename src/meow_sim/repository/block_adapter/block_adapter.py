from src.bdk.base_block import BaseBlock
from src.bdk.block_info import BlockInfo
from src.meow_sim.entity.block_distribution_name import BlockDistributionName
from src.meow_sim.entity.block_id import BlockId


class BlockAdapter:
    distribution_name: BlockDistributionName
    info: BlockInfo
    _block_instance: BaseBlock

    def __init__(self, block_class: BaseBlock):
        self._block_instance = block_class()
        self.info = self._block_instance.get_info()
        self.distribution_name = self.info.distribution_name
