from dataclasses import dataclass
from typing import Any


@dataclass
class ParamDescription:
    key: str
    value: Any
