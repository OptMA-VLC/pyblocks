from dataclasses import dataclass
from enum import Enum, auto
from typing import Any


class ParamType(Enum):
    STRING = auto()


@dataclass
class Parameter:
    type: str = None  # string, int,
    required: bool = False
    default: Any = ''
    value: Any = None
