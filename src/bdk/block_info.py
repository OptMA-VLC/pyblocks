from dataclasses import dataclass

from src.bdk.block_distribution_id import BlockDistributionId


@dataclass
class BlockInfo:
    distribution_id: BlockDistributionId
    name: str
    description: str
