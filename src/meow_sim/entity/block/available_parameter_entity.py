from dataclasses import dataclass
from typing import Type, Any

from src.bdk.params.param_id import ParamId


@dataclass
class AvailableParameterEntity:
    param_id: ParamId
    type: Type = Any
