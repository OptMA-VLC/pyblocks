from dataclasses import dataclass
from typing import Any, Type

from src.bdk.params.param_id import ParamId


@dataclass
class Parameter:
    id: ParamId
    type: Type
    default: Any = None
    value: Any = None
