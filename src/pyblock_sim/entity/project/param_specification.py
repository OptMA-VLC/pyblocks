from dataclasses import dataclass
from typing import Any, Type

from src.pyblock.block.params.param_id import ParamId


@dataclass
class ParamSpecification:
    param_id: ParamId
    value: Any
    type: Type = Any
