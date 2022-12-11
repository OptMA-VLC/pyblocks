from dataclasses import dataclass
from typing import List

from src.meow_sim.config.block_description import BlockDescription
from src.meow_sim.config.connection_description import ConnectionDescription


@dataclass
class Config:
    blocks: List[BlockDescription]
    connections: List[ConnectionDescription]
