from dataclasses import dataclass
from typing import Any, Type

from src.pyblock.block.params.param_id import ParamId


@dataclass
class ParameterEntity:
    param_id: ParamId
    value: Any
    type: Type = Any
