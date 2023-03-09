from dataclasses import dataclass

from src.bdk.block_distribution_id import BlockDistributionId
from src.meow_sim.entity.block_instance_id import BlockInstanceId
from src.meow_sim.repository.block_adapter.block_adapter import BlockAdapter

@dataclass
class Block:
    instance_id: BlockInstanceId
    distribution_id: BlockDistributionId
    name: str
    adapter: BlockAdapter
