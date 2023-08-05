from dataclasses import dataclass, field
from typing import List

from src.pyblock.block.block_distribution_id import BlockDistributionId
from src.pyblock_sim.entity.block.block_instance_id import BlockInstanceId
from src.pyblock_sim.entity.block.parameter_entity import ParameterEntity


@dataclass
class BlockSpecification:
    dist_id: BlockDistributionId
    instance_id: BlockInstanceId
    name: str
    params: List[ParameterEntity] = field(default_factory=list)
