from dataclasses import dataclass
from typing import Any, Type

ParamId = str


@dataclass
class Parameter:
    id: ParamId
    type: Type
    value: Any = None
    required: bool = False
    default: Any = None
