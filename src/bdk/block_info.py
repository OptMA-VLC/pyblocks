from dataclasses import dataclass
from typing import List

from src.bdk.params.parameter import Parameter


@dataclass
class BlockInfo:
    distribution_name: str
    name: str
    description: str

    params: List[Parameter]
