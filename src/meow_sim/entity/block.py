from src.meow_sim.entity.block_distribution_name import BlockDistributionName
from src.meow_sim.entity.block_id import BlockId
from src.meow_sim.entity.param_bundle import ParamBundle
from src.meow_sim.repository.block_adapter.block_adapter import BlockAdapter


class Block:
    id: BlockId
    instance_of: BlockDistributionName
    params: ParamBundle
    adapter: BlockAdapter
