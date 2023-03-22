from dataclasses import dataclass, field
from typing import List

from src.pyblock_sim.entity.block.block_entity import BlockEntity
from src.pyblock_sim.entity.graph.connection_entity import ConnectionEntity


@dataclass
class SimulationStep:
    block: BlockEntity
    input_connections: List[ConnectionEntity] = field(default_factory=list)
