from dataclasses import dataclass

from src.bdk.block_distribution_id import BlockDistributionId
from src.meow_sim.entity.block.block_instance_id import BlockInstanceId
from src.meow_sim.entity.block.interface_block_runtime import IBlockRuntime


@dataclass
class Block:
    instance_id: BlockInstanceId
    distribution_id: BlockDistributionId
    name: str
    runtime: IBlockRuntime
