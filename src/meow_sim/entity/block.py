from dataclasses import dataclass

from src.bdk.block_distribution_id import BlockDistributionId
from src.meow_sim.entity.block_id import BlockId
from src.meow_sim.entity.param_bundle import ParamBundle
from src.meow_sim.repository.block_adapter.block_adapter import BlockAdapter


@dataclass
class Block:
    id: BlockId
    instance_of: BlockDistributionId
    params: ParamBundle
    adapter: BlockAdapter
