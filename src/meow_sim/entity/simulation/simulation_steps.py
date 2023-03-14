from dataclasses import dataclass, field
from typing import List

from src.meow_sim.entity.block.block_entity import BlockEntity
from src.meow_sim.entity.connection import Connection


@dataclass
class SimulationStep:
    block: BlockEntity
    input_connections: List[Connection] = field(default_factory=list)
