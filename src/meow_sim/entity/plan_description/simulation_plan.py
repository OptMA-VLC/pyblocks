from dataclasses import dataclass
from typing import List

from src.meow_sim.entity.plan_description import BlockDescription, ConnectionDescription


@dataclass
class SimulationPlan:
    blocks: List[BlockDescription]
    connections: List[ConnectionDescription]
