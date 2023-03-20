from dataclasses import dataclass
from typing import Any

from src.pyblock.block.params.param_id import ParamId
from src.pyblock_sim.entity.block.block_instance_id import BlockInstanceId


@dataclass
class UserParameterEntity:
    block_instance_id: BlockInstanceId
    param_id: ParamId
    value: Any
