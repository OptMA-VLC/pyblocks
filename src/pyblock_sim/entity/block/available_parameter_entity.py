from dataclasses import dataclass
from typing import Type, Any

from src.pyblock.block.params.param_id import ParamId


@dataclass
class AvailableParameterEntity:
    param_id: ParamId
    type: Type = Any
