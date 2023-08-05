from typing import List
from dataclasses import dataclass

from src.pyblock_sim.entity.project.graph.connection_specification import ConnectionSpecification
from src.pyblock_sim.entity.project.graph.block_specification import BlockSpecification


@dataclass
class GraphSpecification:
    blocks: List[BlockSpecification]
    connections: List[ConnectionSpecification]
