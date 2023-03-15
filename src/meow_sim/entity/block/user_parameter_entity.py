from dataclasses import dataclass
from typing import Any

from src.bdk.params.param_id import ParamId
from src.meow_sim.entity.block.block_instance_id import BlockInstanceId


@dataclass
class UserParameterEntity:
    block_instance_id: BlockInstanceId
    param_id: ParamId
    value: Any
