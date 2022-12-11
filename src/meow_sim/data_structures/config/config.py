from dataclasses import dataclass
from typing import List

from .block_description import BlockDescription
from .connection_description import ConnectionDescription


@dataclass
class Config:
    blocks: List[BlockDescription]
    connections: List[ConnectionDescription]