from dataclasses import dataclass
from typing import Any, Type

ParamId = str


@dataclass
class Parameter:
    id: ParamId
    type: Type
    value: Any = None
    required: bool = True
    default: Any = None
