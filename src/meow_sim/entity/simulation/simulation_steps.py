from dataclasses import dataclass
from typing import Any, Dict, List

from src.bdk.params.param_id import ParamId
from src.meow_sim.entity.block.block_entity import BlockEntity
from src.meow_sim.entity.connection import Connection


@dataclass
class SimulationStep:
    block: BlockEntity
    params: Dict[ParamId, Any]
    input_connections: List[Connection]
