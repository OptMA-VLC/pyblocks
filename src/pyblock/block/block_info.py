from typing import Union

from src.pyblock.block.block_distribution_id import BlockDistributionId


class BlockInfo:
    distribution_id: BlockDistributionId
    name: str
    description: str

    def __init__(
            self, distribution_id: Union[BlockDistributionId, str],
            name: str = '',
            description: str = ''
    ):
        if isinstance(distribution_id, str):
            distribution_id = BlockDistributionId(distribution_id)

        self.distribution_id = distribution_id
        self.name = name
        self.description = description
