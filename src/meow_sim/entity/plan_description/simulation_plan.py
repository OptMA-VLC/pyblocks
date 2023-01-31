from dataclasses import dataclass
from typing import List

from src.meow_sim.entity.plan_description.block_description import BlockDescription
from src.meow_sim.entity.plan_description.connection_description import ConnectionDescription


@dataclass
class SimulationPlan:
    blocks: List[BlockDescription]
    connections: List[ConnectionDescription]
